import stripe
from datetime import date
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status, views, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.throttling import AnonRateThrottle
from .models import Event, Booking, BusinessHours, CompanyProfile
from .serializers import EventSerializer, BookingSerializer, BusinessHoursSerializer, CompanyConfigSerializer
from .services import create_booking, get_available_slots, get_monthly_availability
from .stripe_utils import create_stripe_checkout, get_stripe_client

class CompanyConfigView(views.APIView):
    """
    Returns the company's public configuration (branding, contact, timezone).
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            profile = CompanyProfile.objects.get()
            data = {
                "brand_color": profile.brand_color,
                "logo": profile.logo,
                "currency": profile.currency,
                "contact_email": profile.contact_email,
                "contact_phone": profile.contact_phone,
                "company_name": getattr(request.tenant, 'name', 'Company'),
                "timezone": settings.TIME_ZONE,
            }
            serializer = CompanyConfigSerializer(data, context={'request': request})
            return Response(serializer.data)
        except CompanyProfile.DoesNotExist:
            return Response({"detail": _("Provider configuration is missing.")}, status=404)

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Publicly list and retrieve available events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    @action(detail=True, methods=['get'])
    def calendar(self, request, pk=None):
        """
        Returns a dict mapping YYYY-MM-DD to boolean availability for a month.
        """
        event = self.get_object()
        try:
            year = int(request.query_params.get('year', timezone.now().year))
            month = int(request.query_params.get('month', timezone.now().month))
        except ValueError:
            return Response({"detail": _("Invalid year or month.")}, status=400)
            
        data = get_monthly_availability(event, year, month)
        return Response(data)

    @action(detail=True, methods=['get'])
    def slots(self, request, pk=None):
        """
        Returns a list of available ISO 8601 start times for a given date.
        """
        event = self.get_object()
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({"detail": _("Date parameter is required.")}, status=400)
        try:
            date_obj = date.fromisoformat(date_str)
        except ValueError:
            return Response({"detail": _("Invalid date format. Use YYYY-MM-DD.")}, status=400)
            
        data = get_available_slots(event, date_obj)
        return Response(data)

class BookingViewSet(viewsets.ModelViewSet):
    """
    Endpoint for creating and retrieving appointments.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    throttle_classes = [AnonRateThrottle]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        event = serializer.validated_data["event"]
        success_url = request.data.get("success_url")
        cancel_url = request.data.get("cancel_url")
        
        try:
            # 1. Create the booking (as PENDING)
            booking = create_booking(
                event=event,
                client_name=serializer.validated_data["client_name"],
                client_email=serializer.validated_data["client_email"],
                client_phone=serializer.validated_data.get("client_phone"),
                start_time=serializer.validated_data["start_time"]
            )
            
            # 2. Handle Payment logic
            if event.event_type.payment_model == "PRE-PAID":
                if not success_url or not cancel_url:
                    booking.delete()
                    return Response(
                        {"detail": _("success_url and cancel_url are required for pre-paid bookings.")},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                try:
                    session = create_stripe_checkout(booking, success_url, cancel_url)
                    return Response({
                        "id": booking.id,
                        "status": booking.status,
                        "checkout_url": session.url
                    }, status=status.HTTP_201_CREATED)
                except Exception as e:
                    # Cleanup booking if stripe fails
                    booking.delete()
                    return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            # 3. POST-PAID: Auto-confirm
            booking.status = "CONFIRMED"
            booking.save()
            
            response_serializer = self.get_serializer(booking)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BusinessHoursViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Returns the company's global operating hours.
    """
    queryset = BusinessHours.objects.all()
    serializer_class = BusinessHoursSerializer
    permission_classes = [permissions.AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(views.APIView):
    """
    Handle Stripe webhooks to finalize bookings.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        try:
            profile = CompanyProfile.objects.get()
            webhook_secret = profile.stripe_webhook_secret
            
            if not webhook_secret:
                return Response({"detail": "Webhook secret not configured."}, status=400)
            
            s = get_stripe_client()
            event = s.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=400)

        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            booking_id = session.get('client_reference_id') or session.get('metadata', {}).get('booking_id')
            
            if booking_id:
                try:
                    booking = Booking.objects.get(id=booking_id)
                    booking.status = "PAID"
                    booking.save()
                    
                    # Trigger Google Sync if needed (handled in signals or save?)
                    # scheduler/models.py save() doesn't trigger sync.
                    # scheduler/admin.py has an action for it.
                    # scheduler/google_calendar.py has the logic.
                    try:
                        from .google_calendar import sync_booking_to_google
                        sync_booking_to_google(booking)
                    except ImportError:
                        pass
                        
                except Booking.DoesNotExist:
                    pass

        return Response({"status": "success"})
