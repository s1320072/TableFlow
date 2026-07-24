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
- **URL**: `/reservations/list/`
- **View function**: `apps.reservations.views.reservation_list`
- **Template**: `reservations/list.html`
- **Arguments**: none
- **Return value**: Rendered HTML page with a `reservations` context variable (queryset of `Reservation` objects)

### 3. Reservation form page
- **URL**: `/reservations/new/`
- **View function**: `apps.reservations.views.reservation_form`
- **Template**: `reservations/form.html`
- **Arguments**: none
- **Return value** (GET): Rendered HTML page with an empty `ReservationForm`
- **Return value** (POST): On valid submission, saves the reservation and redirects to the confirmation page. On invalid submission, re-renders the form with validation errors.

> **Note**: Reservation creation is handled via POST on this endpoint. There is no separate `process` endpoint.

### 4. Confirmation page
- **URL**: `/reservations/<pk>/`
- **View function**: `apps.reservations.views.confirmation`
- **Template**: `reservations/confirmation.html`
- **Arguments**: `pk` (integer, path parameter)
- **Return value**: Rendered HTML confirmation page with `reservation` context variable (the created `Reservation` object, with related `table` eagerly loaded)

### 5. Redirect page
- **URL**: `/reservations/redirect/`
- **View function**: `apps.reservations.views.redirect_page`
- **Arguments**: none
- **Return value**: HTTP 302 redirect to `reservation-list`

### 6. Available tables partial (HTMX)
- **URL**: `/reservations/available-tables-partial/`
- **View function**: `apps.reservations.views.available_tables_partial`
- **Template**: `reservations/_table_options.html`
- **Arguments** (GET query string):
  - `reservation_time` (datetime string, optional) — filters out tables booked at that time
  - `num_guests` (integer string, optional) — filters tables to those with `capacity >= num_guests`
- **Return value**: Rendered HTML fragment with `tables` context variable (queryset of active, matching `Table` objects)
