# Capability: Companies i18n and Field Descriptions

## MODIFIED Requirements
### Requirement: Model Localization
The project SHALL provide translated names for models and fields in the `companies` app.

#### Scenario: Translatable Metadata
- **Given** I am in `companies/models.py`
- **When** I check the `Client` and `Domain` models
- **Then** their `verbose_name` and `verbose_name_plural` SHALL be translatable.
- **AND** their fields SHALL have translatable names and help texts.
- **AND** `Client.schema_name` SHALL have verbose_name = _("tenant ID") and help_text = _("Internal identifier used to isolate data. Must be unique and lowercase.")
- **AND** `Client.name` SHALL have verbose_name = _("company name") and help_text = _("Official display name of the tenant.")
- **AND** `Client.is_active` SHALL have verbose_name = _("active status") and help_text = _("Uncheck to suspend all tenant operations.")
- **AND** `Domain.domain` SHALL have verbose_name = _("web address") and help_text = _("The URL where users will access the booking portal (e.g., tenant.com).")
- **AND** `Domain.is_primary` SHALL have verbose_name = _("primary URL") and help_text = _("If multiple domains exist, this is the main address.")
