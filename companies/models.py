from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    schema_name = models.CharField(max_length=63, unique=True)
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # default reverse lookup names are 'tenant' and 'domain'
    auto_create_schema = True

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    domain = models.CharField(max_length=253, unique=True)
    tenant = models.ForeignKey(Client, related_name='domains', on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=True)

    def __str__(self):
        return self.domain
