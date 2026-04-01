# Spec Delta: Infrastructure and Dependencies

## ADDED Requirements

### Requirement: Multi-Tenant and Cryptography Dependencies SHALL be defined
The Multi-Tenant and Cryptography Dependencies SHALL be defined.
Specific versions of the libraries must be used to ensure compatibility with Django 5.2.

#### Scenario: `requirements.txt` updates
- `django-tenants==3.10.1` (Latest stable with Django 5.2 support).
- `django-cryptography-5==2.0.3` (Recommended fork for Django 5.x support).
