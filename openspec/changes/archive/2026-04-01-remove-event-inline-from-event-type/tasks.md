# Tasks: Remove Event Inline from Event Type

## Phase 1: Implementation
- [x] Remove `EventInline` from `scheduler/admin.py`.
- [x] Remove `inlines = [EventInline]` from `EventTypeAdmin`.

## Phase 2: Validation
- [x] Verify `EventType` change form no longer displays the `Event` inline.
