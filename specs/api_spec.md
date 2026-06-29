# API Specification

## Endpoints (Exercise 6 — Server-Rendered Views)

All endpoints are mounted under `/reservations/` in `config/urls.py` and render Django templates (no JSON responses).

### 1. Home page
- **URL**: `/reservations/`
- **View function**: `apps.reservations.views.home`
- **Template**: `reservations/home.html`
- **Arguments**: none
- **Return value**: Rendered HTML page with current server time (`now`)

### 2. List of reservations
- **URL**: `/reservations/reservations/`
- **View function**: `apps.reservations.views.reservation_list`
- **Template**: `reservations/list.html`
- **Arguments**: none
- **Return value**: Rendered HTML page with a `reservations` context variable (list of dicts)

### 3. Reservation form page
- **URL**: `/reservations/reservations/new/`
- **View function**: `apps.reservations.views.reservation_form`
- **Template**: `reservations/form.html`
- **Arguments**: none
- **Return value**: Rendered HTML page with a `<form>` (POSTs to `process-reservation`)

### 4. Process reservation (stub)
- **URL**: `/reservations/reservations/process/`
- **View function**: `apps.reservations.views.process_reservation`
- **Template**: `reservations/confirmation.html`
- **Arguments** (POST):
  - `customer_name` (string)
  - `num_guests` (integer)
  - `reservation_time` (datetime string)
- **Return value** (POST): Rendered confirmation HTML page with submitted data
- **Return value** (GET): Redirect to `reservation-form`

### 5. Redirect page
- **URL**: `/reservations/redirect/`
- **View function**: `apps.reservations.views.redirect_page`
- **Arguments**: none
- **Return value**: HTTP 302 redirect to `reservation-list`
