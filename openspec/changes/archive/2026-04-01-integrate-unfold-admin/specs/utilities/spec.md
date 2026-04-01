# utilities Specification Delta

## ADDED Requirements
### Requirement: Environment Badge Callback
The project SHALL include a callback function to identify the current environment stage in the admin interface.

#### Scenario: Environment Badge Identification
- **Given** I am in `utils/callbacks.py`
- **When** `environment_callback` is executed
- **Then** it SHALL return the environment label and badge color (e.g., ["Production", "danger"]) based on the `ENV` variable.
