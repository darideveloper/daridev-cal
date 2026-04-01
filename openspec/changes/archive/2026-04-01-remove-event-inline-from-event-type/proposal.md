# Proposal: Remove Event Inline from Event Type

## Problem
The `EventType` admin currently has an `Event` inline. While it allows creating services within a category, it creates redundant complexity on the category page when the user's primary goal is managing the category details.

## Proposed Solution
Remove the `EventInline` from the `EventTypeAdmin` to keep the category management page focused. Users will continue to manage events via the dedicated `EventAdmin` page.

## Key Changes
- Remove `EventInline` definition from `scheduler/admin.py`.
- Remove `inlines = [EventInline]` from `EventTypeAdmin`.
