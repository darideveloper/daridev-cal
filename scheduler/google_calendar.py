import logging
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings
from django.urls import reverse
from django.db import connection
from companies.models import Domain
from django.utils import timezone
from .models import Booking, CompanyProfile

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_google_calendar_service(company_profile):
    """
    Initializes the Google Calendar API service using credentials 
    from the CompanyProfile.
    """
    if not company_profile.google_calendar_credentials:
        logger.warning("No Google Calendar credentials found for company profile.")
        return None

    try:
        creds_json = json.loads(company_profile.google_calendar_credentials)
        credentials = service_account.Credentials.from_service_account_info(
            creds_json, scopes=SCOPES
        )
        return build('calendar', 'v3', credentials=credentials)
    except Exception as e:
        logger.error(f"Failed to initialize Google Calendar service: {str(e)}")
        return None

def delete_google_calendar_event(booking):
    """
    Deletes a Google Calendar event associated with a Booking.
    """
    if not booking.google_event_id:
        return

    try:
        company_profile = CompanyProfile.objects.first()
        if not company_profile or not company_profile.google_calendar_id:
            logger.info(f"Skipping deletion for booking {booking.id}: No calendar configured.")
            return

        service = get_google_calendar_service(company_profile)
        if not service:
            return

        calendar_id = company_profile.google_calendar_id
        service.events().delete(
            calendarId=calendar_id, 
            eventId=booking.google_event_id
        ).execute()
        logger.info(f"Deleted Google Calendar event {booking.google_event_id} for booking {booking.id}")
    except HttpError as e:
        if e.resp.status == 404:
            logger.info(f"Google event {booking.google_event_id} already deleted.")
        else:
            logger.error(f"Error deleting Google Calendar event {booking.google_event_id}: {str(e)}")
    except Exception as e:
        logger.error(f"Error deleting Google Calendar event {booking.google_event_id}: {str(e)}")

def sync_booking_to_google(booking, skip_save=False):
    """
    Syncs a Booking to the company's Google Calendar.
    Handles both Insert (new event) and Patch (update existing).
    """
    company_profile = CompanyProfile.objects.first()
    
    if not company_profile or not company_profile.google_calendar_id:
        logger.info(f"Skipping sync for booking {booking.id}: No calendar configured.")
        booking.google_sync_status = "DISABLED"
        if not skip_save:
            booking.save(update_fields=['google_sync_status'])
        return

    service = get_google_calendar_service(company_profile)
    if not service:
        booking.google_sync_status = "FAILURE"
        booking.google_sync_error = "Could not initialize Google Calendar service. Check credentials."
        if not skip_save:
            booking.save(update_fields=['google_sync_status', 'google_sync_error'])
        return

    try:
        # Build absolute URL to the Django Admin edit page
        admin_path = reverse('admin:scheduler_booking_change', args=[booking.id])
        
        # Determine the base URL from the tenant domain
        try:
            domain = Domain.objects.filter(is_primary=True).first()
            if not domain:
                domain = Domain.objects.first()
            base_url = f"https://{domain.domain}" if domain else ""
        except:
            base_url = ""

        admin_url = f"{base_url}{admin_path}" if base_url else admin_path
        
        description = (
            f"Service: {booking.event.title}\n"
            f"Client: {booking.client_name}\n"
            f"Email: {booking.client_email}\n"
            f"Status: {booking.status}\n\n"
            f"--- Admin Link ---\n"
            f"Manage Booking: {admin_url}"
        )

        event_body = {
            'summary': f"{booking.event.title} - {booking.client_name}",
            'description': description,
            'start': {
                'dateTime': booking.start_time.isoformat(),
                'timeZone': settings.TIME_ZONE,
            },
            'end': {
                'dateTime': booking.end_time.isoformat(),
                'timeZone': settings.TIME_ZONE,
            },
            'status': 'confirmed' if booking.status in ["CONFIRMED", "PAID"] else 'tentative',
        }

        calendar_id = company_profile.google_calendar_id

        if booking.google_event_id:
            # Update existing event
            try:
                service.events().patch(
                    calendarId=calendar_id,
                    eventId=booking.google_event_id,
                    body=event_body
                ).execute()
                logger.info(f"Updated Google Calendar event {booking.google_event_id} for booking {booking.id}")
            except HttpError as e:
                if e.resp.status == 404:
                    # Event was deleted on Google, so create it again
                    logger.warning(f"Google event {booking.google_event_id} not found. Re-creating.")
                    event = service.events().insert(calendarId=calendar_id, body=event_body).execute()
                    booking.google_event_id = event['id']
                else:
                    raise e
        else:
            # Create new event
            event = service.events().insert(calendarId=calendar_id, body=event_body).execute()
            booking.google_event_id = event['id']
            logger.info(f"Created Google Calendar event {event['id']} for booking {booking.id}")

        booking.google_sync_status = "SUCCESS"
        booking.google_sync_error = None
        booking.last_synced_at = timezone.now()
        if not skip_save:
            booking.save(update_fields=['google_event_id', 'google_sync_status', 'google_sync_error', 'last_synced_at'])

    except HttpError as e:
        error_msg = str(e)
        logger.error(f"HTTP Error syncing booking {booking.id}: {error_msg}")
        booking.google_sync_status = "FAILURE"
        booking.google_sync_error = error_msg
        if not skip_save:
            booking.save(update_fields=['google_sync_status', 'google_sync_error'])
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error syncing booking {booking.id}: {error_msg}")
        booking.google_sync_status = "FAILURE"
        booking.google_sync_error = error_msg
        if not skip_save:
            booking.save(update_fields=['google_sync_status', 'google_sync_error'])
