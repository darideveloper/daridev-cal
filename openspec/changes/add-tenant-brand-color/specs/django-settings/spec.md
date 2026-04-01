## MODIFIED Requirements
### Requirement: Unfold Brand Customization
The project SHALL configure `django-unfold` in `settings.py` with custom branding and operational features.

#### Scenario: Color Customization
- **Given** I am in `project/settings.py`
- **When** the `UNFOLD["COLORS"]["primary"]` is configured
- **Then** it SHALL prioritize using the CSS variables `var(--color-primary-400)`, `var(--color-primary-500)`, and `var(--color-primary-600)`.
- **And** it SHALL fallback to default OKLCH values for the public schema.
