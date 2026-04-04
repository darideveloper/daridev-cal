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

def get_google_calendar_service():
    """Returns an authorized Google Calendar service object."""
    creds_str = getattr(settings, 'GOOGLE_CALENDAR_CREDENTIALS', None)
    
    if not creds_str:
        logger.error("GOOGLE_CALENDAR_CREDENTIALS is not set or is empty in settings.")
        return None

    try:
        creds_json = json.loads(creds_str)
        credentials = service_account.Credentials.from_service_account_info(
            creds_json, scopes=SCOPES
        )
        return build('calendar', 'v3', credentials=credentials)
    except json.JSONDecodeError as e:
        logger.error(f"GOOGLE_CALENDAR_CREDENTIALS contains invalid JSON: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to initialize centralized Google Calendar service: {e}")
        return None

def create_tenant_calendar(company_profile):
    """
    Programmatically create a new Google Calendar for a tenant using the master account.
    Returns the new calendar ID or None on failure.
    """
    service = get_google_calendar_service()
    if not service:
        return None

    try:
        # 1. Create the Calendar
        calendar_body = {
            'summary': f"Scheduler - {company_profile.contact_email or 'Tenant'}",
            'timeZone': settings.TIME_ZONE
        }
        created_calendar = service.calendars().insert(body=calendar_body).execute()
        calendar_id = created_calendar['id']
        logger.info(f"Created new Google Calendar {calendar_id} for profile {company_profile.id}")

        # 2. Share with the tenant's email (if provided)
        if company_profile.contact_email:
            share_calendar_with_client(calendar_id, company_profile.contact_email)
        
        return calendar_id
    except Exception as e:
        logger.error(f"Error creating tenant calendar: {str(e)}")
        return None

def share_calendar_with_client(calendar_id, client_email):
    """
    Grants 'reader' access to the tenant's primary email for their new calendar.
    """
    service = get_google_calendar_service()
    if not service:
        return

    try:
        rule = {
            'scope': {'type': 'user', 'value': client_email},
            'role': 'reader'
        }
        service.acl().insert(calendarId=calendar_id, body=rule).execute()
        logger.info(f"Shared calendar {calendar_id} with {client_email}")
    except Exception as e:
        logger.warning(f"Failed to share calendar {calendar_id} with {client_email}: {str(e)}")

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

        service = get_google_calendar_service()
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

    service = get_google_calendar_service()
    if not service:
        booking.google_sync_status = "FAILURE"
        booking.google_sync_error = "Could not initialize Google Calendar service. Check centralized credentials."
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
