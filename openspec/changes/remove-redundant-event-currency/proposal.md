# Proposal: Remove Redundant Event Currency

## Problem
The `Event` model currently has a `currency` field that is redundant because each tenant already defines a global `currency` in their `CompanyProfile`. This redundancy leads to potential data inconsistency, a cluttered Admin UI, and complexity in maintaining multiple sources of truth for the same information.

## Solution
Consolidate currency handling at the tenant level by:
1.  Removing the `currency` field from the `Event` model.
2.  Updating the `EventAdmin` to remove the `currency` field from its forms.
3.  Fixing the `EventSerializer` to remove references to the deleted field (and the outdated `format_category` name).
4.  Ensuring that all service-related logic defaults to the `CompanyProfile.currency`.

## Scope
- `scheduler/models.py`: Remove `Event.currency`.
- `scheduler/admin.py`: Remove `currency` from `EventAdmin`.
- `scheduler/serializers.py`: Clean up `EventSerializer`.
- `scheduler/migrations/`: Generate a new migration.
