# Database Schema Specification

## Models
### 1. Table
- `table_number` (CharField, Unique)
- `capacity` (PositiveIntegerField)
- `is_active` (BooleanField)

### 2. Reservation
- `customer_name` (CharField)
- `num_guests` (PositiveIntegerField)
- `reservation_time` (DateTimeField)
- `table` (ForeignKey to Table)
- `status` (CharField, Choices)