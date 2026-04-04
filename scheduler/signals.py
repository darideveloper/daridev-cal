import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Booking, CompanyProfile
from .google_calendar import sync_booking_to_google, delete_google_calendar_event

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Booking)
def booking_post_save(sender, instance, created, update_fields, **kwargs):
    """
    Automated Google Calendar synchronization on booking creation/update.
    """
    # Avoid recursion when we update sync-related fields on the instance
    sync_fields = {'google_event_id', 'google_sync_status', 'google_sync_error', 'last_synced_at'}
    if update_fields and sync_fields.intersection(set(update_fields)):
        return

    # Synchronize the booking in real-time
    try:
        sync_booking_to_google(instance)
    except Exception as e:
        logger.error(f"Failed to sync booking {instance.id} in post_save signal: {str(e)}")

@receiver(post_delete, sender=Booking)
def booking_post_delete(sender, instance, **kwargs):
    """
    Automated Google Calendar event deletion when a booking is deleted.
    """
    try:
        delete_google_calendar_event(instance)
    except Exception as e:
        logger.error(f"Failed to delete booking {instance.id} in post_delete signal: {str(e)}")
@receiver(post_save, sender=CompanyProfile)
def ensure_tenant_google_calendar(sender, instance, created, **kwargs):
    """
    Ensure the tenant has a Google Calendar ID assigned.
    If not, create one using the master service account.
    """
    if not instance.google_calendar_id:
        from .google_calendar import create_tenant_calendar
        calendar_id = create_tenant_calendar(instance)
        if calendar_id:
            logger.info(f"Assigning new calendar ID {calendar_id} to profile {instance.id}")
            # Use update_fields to avoid triggering other signals or logic unexpectedly
            # and to avoid infinite recursion if we were checking for other fields.
            instance.google_calendar_id = calendar_id
            instance.save(update_fields=['google_calendar_id'])
