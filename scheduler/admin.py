from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import CompanyProfile, EventType, Booking

@admin.register(CompanyProfile)
class CompanyProfileAdmin(ModelAdmin):
    pass

@admin.register(EventType)
class EventTypeAdmin(ModelAdmin):
    list_display = ("title", "duration_minutes", "price", "allow_overlap")

@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ("client_name", "event_type", "start_time", "end_time", "status")
    list_filter = ("start_time", "status")
    search_fields = ("client_name", "client_email")
