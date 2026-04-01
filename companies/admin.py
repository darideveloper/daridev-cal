from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from unfold.admin import ModelAdmin
from project.admin import public_admin_site
from .models import Client, Domain

class ClientAdmin(TenantAdminMixin, ModelAdmin):
    list_display = ('schema_name', 'name', 'created_on', 'is_active')
    search_fields = ('schema_name', 'name')

class DomainAdmin(TenantAdminMixin, ModelAdmin):
    pass

public_admin_site.register(Client, ClientAdmin)
public_admin_site.register(Domain, DomainAdmin)
