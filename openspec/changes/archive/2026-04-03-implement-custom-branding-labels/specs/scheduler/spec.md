## ADDED Requirements

### Requirement: Customizable UI Labels
The `CompanyProfile` SHALL include fields to allow tenants to customize the labels used in the frontend booking UI.

#### Scenario: `CompanyProfile` UI label fields
- `event_type_label`: `CharField` (max_length=100, default=_("Event Type")).
- `event_label`: `CharField` (max_length=100, default=_("Event")).
- `availability_free_label`: `CharField` (max_length=100, default=_("Free")).
- `availability_regular_label`: `CharField` (max_length=100, default=_("Regular")).
- `availability_no_free_label`: `CharField` (max_length=100, default=_("Full")).
- `extras_label`: `CharField` (max_length=100, default=_("Extras")).

#### Scenario: Translatable UI labels
- **Given** I am editing the `CompanyProfile` in the admin.
- **Then** the labels and help texts for these new fields SHALL be translatable.
- **AND** they SHALL be organized in a "UI Labels" tab.
