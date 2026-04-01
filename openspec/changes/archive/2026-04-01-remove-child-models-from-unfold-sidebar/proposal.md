# Proposal: Remove Child Models from Unfold Sidebar

## Problem
The Unfold admin sidebar contains links to models that have been unregistered or are now managed exclusively as inlines (e.g., Business Hours, Domains, Availability Rules). Clicking these links results in errors or 404s, creating a poor user experience and visual clutter.

## Proposed Solution
Clean up the `UNFOLD["SIDEBAR"]["navigation"]` configuration in `project/settings.py` by removing the redundant and broken links.

## Key Changes
- Remove "Domains" from the Multi-Tenancy section.
- Remove "Business Hours" from the Scheduling section.
- Remove "Availability Rules" and "Availability Slots" from the Configuration section.
