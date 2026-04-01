from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from project.admin import ModelAdminUnfoldBase
from project.admin import public_admin_site
from .models import Client, Domain

class ClientAdmin(TenantAdminMixin, ModelAdminUnfoldBase):
    list_display = ('schema_name', 'name', 'created_on', 'is_active')
    search_fields = ('schema_name', 'name')

class DomainAdmin(TenantAdminMixin, ModelAdminUnfoldBase):
    pass

public_admin_site.register(Client, ClientAdmin)
public_admin_site.register(Domain, DomainAdmin)
