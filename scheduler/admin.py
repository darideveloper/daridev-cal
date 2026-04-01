from django.contrib import admin
from django.db import models
from django.forms import TextInput
from project.admin import ModelAdminUnfoldBase, tenant_admin_site
from .models import CompanyProfile, EventType, Booking, BusinessHours, Event, EventAvailability, AvailabilitySlot

class CompanyProfileAdmin(ModelAdminUnfoldBase):
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "brand_color":
            kwargs["widget"] = TextInput(attrs={"type": "color"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)

class EventTypeAdmin(ModelAdminUnfoldBase):
    list_display = ("title", "payment_model", "allow_overlap")

class EventAdmin(ModelAdminUnfoldBase):
    list_display = ("title", "event_type", "price", "duration_minutes")
    list_filter = ("event_type",)

class BookingAdmin(ModelAdminUnfoldBase):
    list_display = ("client_name", "event", "start_time", "end_time", "status")
    list_filter = ("start_time", "status")
    search_fields = ("client_name", "client_email")

class BusinessHoursAdmin(ModelAdminUnfoldBase):
    list_display = ("weekday", "start_time", "end_time")
    list_filter = ("weekday",)

class EventAvailabilityAdmin(ModelAdminUnfoldBase):
    list_display = ("event", "start_date", "end_date")

class AvailabilitySlotAdmin(ModelAdminUnfoldBase):
    list_display = ("event_availability", "weekday", "start_time", "end_time")
    list_filter = ("weekday",)

tenant_admin_site.register(CompanyProfile, CompanyProfileAdmin)
tenant_admin_site.register(EventType, EventTypeAdmin)
tenant_admin_site.register(Booking, BookingAdmin)
tenant_admin_site.register(BusinessHours, BusinessHoursAdmin)
tenant_admin_site.register(Event, EventAdmin)
tenant_admin_site.register(EventAvailability, EventAvailabilityAdmin)
tenant_admin_site.register(AvailabilitySlot, AvailabilitySlotAdmin)
