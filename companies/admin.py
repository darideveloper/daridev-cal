from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from unfold.admin import ModelAdmin
from .models import Client, Domain

@admin.register(Client)
class ClientAdmin(TenantAdminMixin, ModelAdmin):
    list_display = ('schema_name', 'name', 'created_on', 'is_active')
    search_fields = ('schema_name', 'name')

@admin.register(Domain)
class DomainAdmin(TenantAdminMixin, ModelAdmin):
    pass
