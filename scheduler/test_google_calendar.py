from unittest.mock import patch, MagicMock
from django.conf import settings
from zoneinfo import ZoneInfo
from django_tenants.test.cases import TenantTestCase
from django_tenants.utils import schema_context
from datetime import datetime, timedelta
from .models import CompanyProfile, EventType, Event, Booking
from .google_calendar import sync_booking_to_google

class GoogleCalendarSyncTest(TenantTestCase):
    def setUp(self):
        super().setUp()
        with schema_context(self.tenant.schema_name):
            # Setup company with "fake" credentials
            self.company = CompanyProfile.objects.create(
                google_calendar_id="test-calendar@gmail.com",
                google_calendar_credentials='{"type": "service_account", "project_id": "test"}'
            )
            self.event_type = EventType.objects.create(title="Testing", allow_overlap=True)
            self.event = Event.objects.create(
                event_type=self.event_type,
                title="Google Sync Test",
                duration_minutes=30
            )
            self.start_time = datetime(2026, 6, 1, 10, 0, tzinfo=ZoneInfo(settings.TIME_ZONE))

    @patch('scheduler.google_calendar.build')
    @patch('scheduler.google_calendar.service_account.Credentials.from_service_account_info')
    def test_signal_triggers_sync_on_create(self, mock_creds, mock_build):
        """
        Verify that creating a booking triggers the Google Calendar sync via Signal.
        """
        # Mock Google API response
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_service.events().insert().execute.return_value = {'id': 'google_id_123'}

        with schema_context(self.tenant.schema_name):
            # Create booking (triggers post_save signal)
            booking = Booking.objects.create(
                event=self.event,
                client_name="Alice",
                client_email="alice@test.com",
                start_time=self.start_time,
                status="CONFIRMED"
            )

            # Check if google_event_id was updated
            booking.refresh_from_db()
            self.assertEqual(booking.google_event_id, 'google_id_123')
            
            # Verify the mock was called
            self.assertTrue(mock_service.events().insert.called)
            
            # Verify description contains the admin link
            insert_args = mock_service.events().insert.call_args
            description = insert_args.kwargs['body']['description']
            self.assertIn("--- Admin Link ---", description)
            self.assertIn("/admin/scheduler/booking/", description)

    @patch('scheduler.google_calendar.build')
    @patch('scheduler.google_calendar.service_account.Credentials.from_service_account_info')
    def test_signal_triggers_sync_on_update(self, mock_creds, mock_build):
        """
        Verify that updating a booking triggers a 'patch' instead of 'insert'.
        """
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        with schema_context(self.tenant.schema_name):
            # Pre-existing booking with an ID
            booking = Booking.objects.create(
                event=self.event,
                client_name="Bob",
                client_email="bob@test.com",
                start_time=self.start_time,
                google_event_id="old_google_id"
            )
            
            # Update booking
            booking.client_name = "Robert"
            booking.save()

            # Verify that patch was called
            self.assertTrue(mock_service.events().patch.called)
            # Verify it was called with the correct eventId
            call_args = mock_service.events().patch.call_args
            self.assertEqual(call_args.kwargs['eventId'], "old_google_id")

    @patch('scheduler.google_calendar.build')
    @patch('scheduler.google_calendar.service_account.Credentials.from_service_account_info')
    def test_sync_handles_missing_credentials_gracefully(self, mock_creds, mock_build):
        """
        If credentials are missing, sync should skip without error.
        """
        with schema_context(self.tenant.schema_name):
            # Remove credentials
            self.company.google_calendar_credentials = None
            self.company.save()
            
            # This should NOT crash and NOT call Google API
            booking = Booking.objects.create(
                event=self.event,
                client_name="NoCreds",
                client_email="nocreds@test.com",
                start_time=self.start_time
            )
            
            self.assertFalse(mock_build.called)
            self.assertIsNone(booking.google_event_id)

    @patch('scheduler.google_calendar.build')
    @patch('scheduler.google_calendar.service_account.Credentials.from_service_account_info')
    def test_sync_recreation_on_404(self, mock_creds, mock_build):
        """
        If a patch fails with 404 (event deleted in Google), 
        it should re-create the event.
        """
        from googleapiclient.errors import HttpError
        
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Mock patch to raise 404 HttpError
        resp = MagicMock(status=404)
        mock_service.events().patch().execute.side_effect = HttpError(resp, b'Not Found')
        
        # Mock insert to return a new ID
        mock_service.events().insert().execute.return_value = {'id': 'new_google_id'}

        with schema_context(self.tenant.schema_name):
            booking = Booking.objects.create(
                event=self.event,
                client_name="Charlie",
                client_email="charlie@test.com",
                start_time=self.start_time,
                google_event_id="deleted_on_google"
            )
            
            # Save again to trigger sync (patch)
            booking.client_name = "Charlie Updated"
            booking.save()

            booking.refresh_from_db()
            self.assertEqual(booking.google_event_id, 'new_google_id')
            self.assertEqual(booking.google_sync_status, 'SUCCESS')
            self.assertTrue(mock_service.events().insert.called)

    @patch('scheduler.google_calendar.build')
    @patch('scheduler.google_calendar.service_account.Credentials.from_service_account_info')
    def test_sync_failure_handling_403(self, mock_creds, mock_build):
        """
        If a sync fails with 403 (Permission Denied), 
        the status should be updated to FAILURE.
        """
        from googleapiclient.errors import HttpError
        
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Mock insert to raise 403 HttpError
        resp = MagicMock(status=403)
        mock_service.events().insert().execute.side_effect = HttpError(resp, b'Forbidden')

        with schema_context(self.tenant.schema_name):
            booking = Booking.objects.create(
                event=self.event,
                client_name="Dave",
                client_email="dave@test.com",
                start_time=self.start_time
            )
            
            booking.refresh_from_db()
            self.assertEqual(booking.google_sync_status, 'FAILURE')
            self.assertIn('Forbidden', booking.google_sync_error)

    @patch('scheduler.google_calendar.build')
    @patch('scheduler.google_calendar.service_account.Credentials.from_service_account_info')
    def test_deletion_sync(self, mock_creds, mock_build):
        """
        Verify that deleting a booking triggers the Google Calendar event deletion.
        """
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        with schema_context(self.tenant.schema_name):
            booking = Booking.objects.create(
                event=self.event,
                client_name="Eve",
                client_email="eve@test.com",
                start_time=self.start_time,
                google_event_id="google_id_to_delete"
            )
            
            # Delete booking
            booking.delete()

            # Verify that delete was called
            self.assertTrue(mock_service.events().delete.called)
            call_args = mock_service.events().delete.call_args
            self.assertEqual(call_args.kwargs['eventId'], "google_id_to_delete")

    @patch('scheduler.google_calendar.build')
    @patch('scheduler.google_calendar.service_account.Credentials.from_service_account_info')
    def test_manual_sync_action(self, mock_creds, mock_build):
        """
        Verify the admin action logic for manual sync.
        """
        from scheduler.admin import BookingAdmin
        from django.contrib.admin.sites import AdminSite
        
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_service.events().insert().execute.return_value = {'id': 'manual_sync_id'}

        with schema_context(self.tenant.schema_name):
            booking = Booking.objects.create(
                event=self.event,
                client_name="Frank",
                client_email="frank@test.com",
                start_time=self.start_time
            )
            
            # Manually clear sync status to simulate a need for retry
            booking.google_sync_status = 'PENDING'
            booking.save(update_fields=['google_sync_status'])
            
            # Setup admin
            site = AdminSite()
            admin = BookingAdmin(Booking, site)
            
            # Trigger action
            queryset = Booking.objects.filter(id=booking.id)
            admin.retry_google_sync(None, queryset)
            
            booking.refresh_from_db()
            self.assertEqual(booking.google_sync_status, 'SUCCESS')
            self.assertEqual(booking.google_event_id, 'manual_sync_id')
