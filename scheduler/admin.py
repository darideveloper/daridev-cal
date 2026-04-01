from django.contrib import admin
from django.db import models
from django.forms import TextInput
from project.admin import ModelAdminUnfoldBase, tenant_admin_site
from .models import CompanyProfile, EventType, Booking

class CompanyProfileAdmin(ModelAdminUnfoldBase):
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "brand_color":
            kwargs["widget"] = TextInput(attrs={"type": "color"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)

class EventTypeAdmin(ModelAdminUnfoldBase):
    list_display = ("title", "duration_minutes", "price", "allow_overlap")

class BookingAdmin(ModelAdminUnfoldBase):
    list_display = ("client_name", "event_type", "start_time", "end_time", "status")
    list_filter = ("start_time", "status")
    search_fields = ("client_name", "client_email")

tenant_admin_site.register(CompanyProfile, CompanyProfileAdmin)
tenant_admin_site.register(EventType, EventTypeAdmin)
tenant_admin_site.register(Booking, BookingAdmin)
