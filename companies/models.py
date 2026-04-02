from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.utils.translation import gettext_lazy as _

class Client(TenantMixin):
    schema_name = models.CharField(
        _("tenant ID"), 
        max_length=63, 
        unique=True,
        help_text=_("Internal identifier used to isolate data. Must be unique and lowercase.")
    )
    name = models.CharField(
        _("company name"), 
        max_length=100,
        help_text=_("Official display name of the tenant.")
    )
    created_on = models.DateField(_("created on"), auto_now_add=True)
    is_active = models.BooleanField(
        _("active status"), 
        default=True,
        help_text=_("Uncheck to suspend all tenant operations.")
    )
    
    # default reverse lookup names are 'tenant' and 'domain'
    auto_create_schema = True

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    domain = models.CharField(
        _("web address"), 
        max_length=253, 
        unique=True,
        help_text=_("The URL where users will access the booking portal (e.g., tenant.com).")
    )
    tenant = models.ForeignKey(
        Client, 
        related_name='domains', 
        on_delete=models.CASCADE, 
        verbose_name=_("tenant")
    )
    is_primary = models.BooleanField(
        _("primary URL"), 
        default=True,
        help_text=_("If multiple domains exist, this is the main address.")
    )

    class Meta:
        verbose_name = _("Domain")
        verbose_name_plural = _("Domains")

    def __str__(self):
        return self.domain
