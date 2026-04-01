# spec.md (django-settings)

## MODIFIED Requirements

### Requirement: Unfold Brand Customization
The project SHALL configure `django-unfold` in `settings.py` with custom branding and operational features.

#### MODIFIED Scenario: Sidebar Configuration
- **GIVEN** the `UNFOLD` settings
- **WHEN** the sidebar is rendered
- **THEN** it MUST NOT contain entries for child models that are managed via inlines, specifically:
    - `Domains` (Public Admin)
    - `Business Hours` (Tenant Admin)
    - `Availability Rules` (Tenant Admin)
    - `Availability Slots` (Tenant Admin)
