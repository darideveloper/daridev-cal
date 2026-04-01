from django.contrib import admin
from project.admin import ModelAdminUnfoldBase
from project.admin import tenant_admin_site
from .models import CompanyProfile, EventType, Booking

class CompanyProfileAdmin(ModelAdminUnfoldBase):
    pass

class EventTypeAdmin(ModelAdminUnfoldBase):
    list_display = ("title", "duration_minutes", "price", "allow_overlap")

class BookingAdmin(ModelAdminUnfoldBase):
    list_display = ("client_name", "event_type", "start_time", "end_time", "status")
    list_filter = ("start_time", "status")
    search_fields = ("client_name", "client_email")

tenant_admin_site.register(CompanyProfile, CompanyProfileAdmin)
tenant_admin_site.register(EventType, EventTypeAdmin)
tenant_admin_site.register(Booking, BookingAdmin)
