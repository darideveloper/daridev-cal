# Spec: Admin Theme

## MODIFIED Requirements

### Requirement: Display Language Switcher

The Unfold admin theme MUST display a UI control for switching languages.

#### Scenario: Admin Interface
- **GIVEN** the `UNFOLD` settings dictionary
- **WHEN** an admin page is rendered
- **THEN** the `SHOW_LANGUAGES` key must be set to `True`.
