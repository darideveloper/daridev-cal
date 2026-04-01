# Proposal: Remove Logo Preview from Company Profile Admin

## Problem
The `logo_preview` field in the `CompanyProfile` admin is requested to be removed to simplify the interface.

## Proposed Solution
Remove the `logo_preview` method and its reference in `readonly_fields` from the `CompanyProfileAdmin` in `scheduler/admin.py`.

## Key Changes
- Remove `logo_preview` method from `CompanyProfileAdmin`.
- Remove `readonly_fields = ("logo_preview",)` from `CompanyProfileAdmin`.
