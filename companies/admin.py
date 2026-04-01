from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from unfold.admin import TabularInline
from project.admin import ModelAdminUnfoldBase
from project.admin import public_admin_site
from .models import Client, Domain

class DomainInline(TabularInline):
    model = Domain
    extra = 1

class ClientAdmin(TenantAdminMixin, ModelAdminUnfoldBase):
    list_display = ('schema_name', 'name', 'created_on', 'is_active')
    search_fields = ('schema_name', 'name')
    inlines = [DomainInline]

class DomainAdmin(ModelAdminUnfoldBase):
    pass

public_admin_site.register(Client, ClientAdmin)
# Domain is managed via Client inline
# public_admin_site.register(Domain, DomainAdmin)
