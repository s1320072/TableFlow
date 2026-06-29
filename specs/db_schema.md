# Database Schema Specification

## App structure
All apps live under `apps/`:
- `apps/reservations` — booking lifecycle, table assignment, capacity rules
- `apps/accounts` — user authentication and role management
- `apps/api` — DRF endpoints for frontend integration
- `apps/web` — client-facing server-rendered reservation forms and calendar

_Python module path: `apps.reservations.models`_

## Models
### 1. Table (`apps/reservations/models.py`)
- `table_number` (CharField, Unique)
- `capacity` (PositiveIntegerField)
- `is_active` (BooleanField)

### 2. Reservation (`apps/reservations/models.py`)
- `customer_name` (CharField)
- `num_guests` (PositiveIntegerField)
- `reservation_time` (DateTimeField)
- `table` (ForeignKey to Table)
- `status` (CharField, Choices)