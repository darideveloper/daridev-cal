import stripe
from django.conf import settings
from .models import CompanyProfile, Booking

def get_stripe_client():
    """
    Returns a configured stripe module or raises error if not configured.
    """
    profile = CompanyProfile.objects.get()
    if not profile.stripe_secret_key:
        return None
    stripe.api_key = profile.stripe_secret_key
    return stripe

def create_stripe_checkout(booking, success_url, cancel_url):
    """
    Creates a Stripe Checkout Session for a booking.
    """
    profile = CompanyProfile.objects.get()
    s = get_stripe_client()
    
    if not s:
        raise ValueError("Stripe is not configured for this provider.")

    # Price in cents
    amount_cents = int(booking.event.price * 100)
    
    session = s.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": profile.currency.lower(),
                "product_data": {
                    "name": booking.event.title,
                },
                "unit_amount": amount_cents,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
        client_reference_id=str(booking.id),
        customer_email=booking.client_email,
        metadata={
            "booking_id": booking.id,
        }
    )
    return session
