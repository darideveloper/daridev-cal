# Proposal: Update Event Model Currency and Admin UI

## Problem
The `Event` model uses a generic `format_category` field which is no longer appropriate. The system needs to support a specific set of currencies (MXN, USD, EUR). Additionally, the `image_preview` in the `Event` admin is requested to be removed to simplify the interface.

## Proposed Solution
- Rename `format_category` to `currency` in the `Event` model.
- Restrict `currency` choices to: MXN, USD, EUR.
- Remove the `image_preview` from the `EventAdmin` in `scheduler/admin.py`.

## Key Changes
- Update `scheduler/models.py` with the renamed field and choices.
- Update `scheduler/admin.py` to remove `image_preview` logic and update tabs.
- Create and apply migrations.
