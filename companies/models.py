from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.utils.translation import gettext_lazy as _

class Client(TenantMixin):
    schema_name = models.CharField(_("schema name"), max_length=63, unique=True)
    name = models.CharField(_("name"), max_length=100)
    created_on = models.DateField(_("created on"), auto_now_add=True)
    is_active = models.BooleanField(_("is active"), default=True)
    
    # default reverse lookup names are 'tenant' and 'domain'
    auto_create_schema = True

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    domain = models.CharField(_("domain"), max_length=253, unique=True)
    tenant = models.ForeignKey(Client, related_name='domains', on_delete=models.CASCADE, verbose_name=_("tenant"))
    is_primary = models.BooleanField(_("is primary"), default=True)

    class Meta:
        verbose_name = _("Domain")
        verbose_name_plural = _("Domains")

    def __str__(self):
        return self.domain
