from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from unfold.contrib.filters.admin import RangeDateFilter
from unfold.decorators import action
from project.admin import ModelAdminUnfoldBase, tenant_admin_site
from .models import (
    CompanyProfile, CompanyAvailability, CompanyWeekdaySlot, CompanyDateOverride,
    EventType, Booking, Event, EventAvailability, AvailabilitySlot, EventDateOverride
)
from .google_calendar import sync_booking_to_google

class CompanyAvailabilityInline(TabularInline):
    model = CompanyAvailability
    extra = 1
    show_change_link = True
    tab = True

class CompanyWeekdaySlotInline(TabularInline):
    model = CompanyWeekdaySlot
    extra = 0
    show_change_link = True
    tab = True

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.weekday_slots.exists():
            return 0
        return 7

    def get_formset(self, request, obj=None, **kwargs):
        FormSet = super().get_formset(request, obj, **kwargs)
        class InitialFormSet(FormSet):
            def __init__(self, *args, **kwargs):
                if not kwargs.get("initial") and (obj is None or not obj.weekday_slots.exists()):
                    kwargs["initial"] = [{"weekday": i} for i in range(7)]
                super().__init__(*args, **kwargs)
        return InitialFormSet

class CompanyDateOverrideInline(TabularInline):
    model = CompanyDateOverride
    fields = ("date", "is_available", "start_time", "end_time")
    extra = 1
    show_change_link = True
    tab = True

class CompanyProfileAdmin(ModelAdminUnfoldBase):
    inlines = [CompanyAvailabilityInline, CompanyWeekdaySlotInline, CompanyDateOverrideInline]

    tabs = [
        (_("Business Info"), [
            "logo", "brand_color", "currency", 
            "contact_email", "contact_phone",
            "stripe_public_key", "stripe_secret_key", "stripe_webhook_secret",
            "google_calendar_id", "google_calendar_credentials"
        ]),
        (_("Global Date Ranges"), ["availability_rules"]),
        (_("Standard Business Hours"), ["weekday_slots"]),
        (_("Global Overrides"), ["date_overrides"]),
        (_("UI Labels"), [
            "event_type_label", "event_label", 
            "availability_free_label", "availability_regular_label", "availability_no_free_label",
            "extras_label"
        ]),
    ]
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):

        if db_field.name == "brand_color":
            kwargs["widget"] = TextInput(attrs={"type": "color"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class EventTypeAdmin(ModelAdminUnfoldBase):
    list_display = ("title", "payment_model", "allow_overlap")

class EventAvailabilityInline(TabularInline):
    model = EventAvailability
    extra = 1
    show_change_link = True
    tab = True

class EventDateOverrideInline(TabularInline):
    model = EventDateOverride
    fields = ("date", "is_available", "start_time", "end_time")
    extra = 1
    show_change_link = True
    tab = True

class AvailabilitySlotInline(TabularInline):
    model = AvailabilitySlot
    extra = 0
    show_change_link = True
    tab = True

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.availability_slots.exists():
            return 0
        return 7

    def get_formset(self, request, obj=None, **kwargs):
        FormSet = super().get_formset(request, obj, **kwargs)
        class InitialFormSet(FormSet):
            def __init__(self, *args, **kwargs):
                if not kwargs.get("initial") and (obj is None or not obj.availability_slots.exists()):
                    kwargs["initial"] = [{"weekday": i} for i in range(7)]
                super().__init__(*args, **kwargs)
        return InitialFormSet

class BookingInline(TabularInline):
    model = Booking
    extra = 0
    max_num = 0
    hide_title = True
    fields = ("client_name", "client_email", "start_time", "end_time", "status", "manage_booking")
    readonly_fields = ("client_name", "client_email", "start_time", "end_time", "status", "manage_booking")
    can_delete = False
    show_change_link = False
    tab = True

    def manage_booking(self, obj):
        if not obj.pk:
            return ""
        url = reverse("admin:scheduler_booking_change", args=[obj.pk])
        return format_html(
            '<a class="bg-primary-600 font-medium px-4 py-1 rounded-md text-white text-xs inline-block" href="{}">{}</a>',
            url,
            _("Manage")
        )
    manage_booking.short_description = _("Action")

class EventAdmin(ModelAdminUnfoldBase):
    list_display = ("title", "event_type", "price", "duration_minutes")
    list_filter = ("event_type",)
    inlines = [EventAvailabilityInline, EventDateOverrideInline, AvailabilitySlotInline, BookingInline]

    tabs = [
        (_("General"), ["title", "event_type", "image", "description", "detailed_description", "price", "duration_minutes"]),
        (_("Date Ranges"), ["availability_rules"]),
        (_("Weekly Slots"), ["availability_slots"]),
        (_("Date Overrides"), ["date_overrides"]),
        (_("Bookings"), ["view_bookings_link", "bookings"]),
    ]

    def view_bookings_link(self, obj):
        if not obj.pk:
            return ""
        url = reverse("admin:scheduler_booking_changelist")
        return format_html(
            '<a class="bg-primary-600 font-medium px-4 py-2 rounded-md text-white inline-block mb-4" href="{}?event__id__exact={}">{}</a>',
            url,
            obj.pk,
            _("View All Bookings for this Event")
        )
    view_bookings_link.short_description = _("All Bookings")


class BusinessHoursAdmin(ModelAdminUnfoldBase):
    list_display = ("weekday", "start_time", "end_time")
    list_filter = ("weekday",)

class EventAvailabilityAdmin(ModelAdminUnfoldBase):
    list_display = ("event", "start_date", "end_date")

class AvailabilitySlotAdmin(ModelAdminUnfoldBase):
    list_display = ("event", "weekday", "start_time", "end_time")
    list_filter = ("weekday",)

class BookingAdmin(ModelAdminUnfoldBase):
    list_display = ("client_name", "event", "start_time", "status", "google_sync_status")
    list_filter = (
        ("start_time", RangeDateFilter),
        "event",
        "status",
        "google_sync_status",
    )
    search_fields = ("client_name", "client_email")
    readonly_fields = ("google_event_id", "google_sync_status", "google_sync_error", "last_synced_at")
    actions = ["retry_google_sync"]

    @action(description=_("Retry Google Calendar Sync"))
    def retry_google_sync(self, request, queryset):
        for booking in queryset:
            sync_booking_to_google(booking)
        self.message_user(request, _("Google Calendar synchronization triggered for %d bookings.") % queryset.count())

tenant_admin_site.register(CompanyProfile, CompanyProfileAdmin)
tenant_admin_site.register(EventType, EventTypeAdmin)
tenant_admin_site.register(Booking, BookingAdmin)
# BusinessHours is managed via CompanyProfile inline
# tenant_admin_site.register(BusinessHours, BusinessHoursAdmin)
tenant_admin_site.register(Event, EventAdmin)
tenant_admin_site.register(EventAvailability, EventAvailabilityAdmin)
# AvailabilitySlot is managed via Event inline
# tenant_admin_site.register(AvailabilitySlot, AvailabilitySlotAdmin)
