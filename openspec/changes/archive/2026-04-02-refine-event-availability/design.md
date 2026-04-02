# Design Document: Refined Event Availability

## Architecture Overview
This change refines the availability matrix to support specific day overrides with custom hours.

### Hierarchical Availability Matrix (Updated)
When validating a booking for a specific `date` and `time_range`, the logic will be:

1.  **Check `EventDateOverride`**:
    -   If an override exists for the `date`:
        -   If `is_available = False`: **REJECT** (Date is blocked).
        -   If `is_available = True`:
            -   If `start_time` and `end_time` are provided:
                -   If `time_range` fits within `[override.start_time, override.end_time]`: **ACCEPT**.
                -   Else: **REJECT** (Outside custom override hours).
            -   Else (no custom hours): Proceed to **Step 2 (Weekly Slots)**.
2.  **Check `EventAvailability` (Date Range)**:
    -   If no override exists AND `EventAvailability` records exist for the event:
        -   If `date` is outside all `EventAvailability` ranges: **REJECT**.
3.  **Check Weekly Windows**:
    -   **Event-Specific Slots**: If `AvailabilitySlot` records exist for the event on this `weekday`:
        -   If `time_range` fits within any `AvailabilitySlot`: **ACCEPT**.
        -   Else: **REJECT**.
    -   **Global Business Hours**: If NO `AvailabilitySlot` exists for this event/weekday:
        -   If `time_range` fits within any `BusinessHours` for this `weekday`: **ACCEPT**.
        -   Else: **REJECT**.

### Validation Consolidation
The `Booking.clean()` method will be updated to act as a wrapper for `services.validate_booking_time()`. This ensures that any change to the validation logic in the service layer automatically applies to both API bookings and Admin creations.

### Model Changes
- `EventDateOverride`: Add `start_time` (TimeField, null=True, blank=True) and `end_time` (TimeField, null=True, blank=True).

### Administrative UX Hints
To clarify the priority to the user, the following help texts will be added (using `gettext_lazy` for EN/ES):

-   **EventDateOverride**: "Individual date exception. It has the highest priority and overrides Date Ranges. If start/end times are set, they override weekly slots."
    -   *Spanish*: "Excepción de fecha individual. Tiene la máxima prioridad y anula los Rangos de Fechas. Si se establecen horas de inicio/fin, estas anularán los espacios semanales."
-   **EventAvailability**: "Defines the validity period of the event. Note: You still need to define 'Bookable Slots' below for these days to be active."
    -   *Spanish*: "Define el periodo de validez del evento. Nota: Aún debe definir 'Espacios Reservables' abajo para que estos días estén activos."
-   **AvailabilitySlot**: "Weekly pattern for this service. If any slot is defined here, the company's global 'Operating Hours' will be ignored for this event."
    -   *Spanish*: "Patrón semanal para este servicio. Si se define algún espacio aquí, se ignorarán las 'Horas de Operación' globales de la empresa para este evento."
