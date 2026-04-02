from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from unfold.contrib.filters.admin import RangeDateFilter
from project.admin import ModelAdminUnfoldBase, tenant_admin_site
from .models import CompanyProfile, EventType, Booking, BusinessHours, Event, EventAvailability, AvailabilitySlot, EventDateOverride

class BusinessHoursInline(TabularInline):
    model = BusinessHours
    extra = 0
    show_change_link = True
    tab = True

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.business_hours.exists():
            return 0
        return 7

    def get_formset(self, request, obj=None, **kwargs):
        FormSet = super().get_formset(request, obj, **kwargs)
        class InitialFormSet(FormSet):
            def __init__(self, *args, **kwargs):
                if not kwargs.get("initial") and (obj is None or not obj.business_hours.exists()):
                    kwargs["initial"] = [{"weekday": i} for i in range(7)]
                super().__init__(*args, **kwargs)
        return InitialFormSet

class CompanyProfileAdmin(ModelAdminUnfoldBase):
    inlines = [BusinessHoursInline]
    
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
    readonly_fields = ("client_name", "client_email", "start_time", "end_time", "status")
    can_delete = False
    show_change_link = True
    tab = True
    classes = ["collapse"]

class EventAdmin(ModelAdminUnfoldBase):
    list_display = ("title", "event_type", "price", "duration_minutes")
    list_filter = ("event_type",)
    inlines = [EventAvailabilityInline, EventDateOverrideInline, AvailabilitySlotInline, BookingInline]

    tabs = [
        (_("General"), ["title", "event_type", "image", "description", "detailed_description", "price", "duration_minutes"]),
    ]

class BusinessHoursAdmin(ModelAdminUnfoldBase):
    list_display = ("weekday", "start_time", "end_time")
    list_filter = ("weekday",)

class EventAvailabilityAdmin(ModelAdminUnfoldBase):
    list_display = ("event", "start_date", "end_date")

class AvailabilitySlotAdmin(ModelAdminUnfoldBase):
    list_display = ("event", "weekday", "start_time", "end_time")
    list_filter = ("weekday",)

class BookingAdmin(ModelAdminUnfoldBase):
    list_display = ("client_name", "event", "start_time", "end_time", "status")
    list_filter = ("start_time", "status")
    search_fields = ("client_name", "client_email")

tenant_admin_site.register(CompanyProfile, CompanyProfileAdmin)
tenant_admin_site.register(EventType, EventTypeAdmin)
tenant_admin_site.register(Booking, BookingAdmin)
# BusinessHours is managed via CompanyProfile inline
# tenant_admin_site.register(BusinessHours, BusinessHoursAdmin)
tenant_admin_site.register(Event, EventAdmin)
tenant_admin_site.register(EventAvailability, EventAvailabilityAdmin)
# AvailabilitySlot is managed via Event inline
# tenant_admin_site.register(AvailabilitySlot, AvailabilitySlotAdmin)
