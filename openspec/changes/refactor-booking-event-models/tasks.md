# Tasks: Refactor Booking & Event Models

This project is broken down into four phases: core model implementation, business logic implementation, API integration, and finalization.

## Phase 1: Core Model Implementation

- [ ] **1.1.** Modify `scheduler/models.py`: Add the `currency` field to the `CompanyProfile` model.
- [ ] **1.2.** Modify `scheduler/models.py`: Create the new `BusinessHours` model.
- [ ] **1.3.** Modify `scheduler/models.py`: Refactor the `EventType` model, removing fields as specified in the design.
- [ ] **1.4.** Modify `scheduler/models.py`: Create the new `Event` model.
- [ ] **1.5.** Modify `scheduler/models.py`: Create the new `EventAvailability` model (normalized).
- [ ] **1.6.** Modify `scheduler/models.py`: Create the new `AvailabilitySlot` model.
- [ ] **1.7.** Modify `scheduler/models.py`: Update the `Booking` model to link to `Event` and ensure `end_time` calculation is correct.
- [ ] **1.8.** Modify `scheduler/admin.py`: Register the new `BusinessHours`, `Event`, `EventAvailability`, and `AvailabilitySlot` models.
- [ ] **1.9.** Generate Django migrations for the `scheduler` app and review the generated migration file for correctness.

## Phase 2: Business Logic & Testing

- [ ] **2.1.** Create `scheduler/services.py`: Implement the business logic for booking creation and hierarchical validation (checking `EventAvailability` slots then `BusinessHours`).
- [ ] **2.2.** Write unit tests for the new models to verify field types, constraints, and relationships.
- [ ] **2.3.** Write comprehensive unit tests for the booking validation logic, covering all scenarios outlined in the `booking-logic` spec (e.g., valid bookings, rejections, fallbacks).

## Phase 3: API & Integration

- [ ] **3.1.** Refactor API views and serializers responsible for creating and retrieving bookings to align with the new `Event`-based structure.
- [ ] **3.2.** Write integration tests for the updated API endpoints to ensure the full booking workflow functions correctly with the new availability rules.

## Phase 4: Finalization & Data Migration

- [ ] **4.1.** Apply the generated migrations to the database.
- [ ] **4.2.** (Optional, if required) Create a Django data migration script to port any existing production data from the old `EventType` structure to the new `Event` structure, preserving historical bookings.
