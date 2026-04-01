from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Event, Booking, BusinessHours
from .serializers import EventSerializer, BookingSerializer, BusinessHoursSerializer
from .services import create_booking

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Publicly list and retrieve available events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [] # Publicly accessible for booking

class BookingViewSet(viewsets.ModelViewSet):
    """
    Endpoint for creating and retrieving appointments.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Use service layer for data-consistent creation
        try:
            booking = create_booking(
                event=serializer.validated_data["event"],
                client_name=serializer.validated_data["client_name"],
                client_email=serializer.validated_data["client_email"],
                start_time=serializer.validated_data["start_time"]
            )
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
    permission_classes = []
