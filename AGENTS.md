# AGENTS.md

## Project scope

[cite_start]This is a Django app for managing restaurant table capacities, user accounts, and smart reservation workflows (TableFlow)[cite: 19, 20].

Main apps:
- [cite_start]`apps/reservations` — booking lifecycle, table assignment, and capacity rules [cite: 3, 23]
- [cite_start]`apps/accounts` — user authentication and role management [cite: 3, 24]
- `apps/api` — DRF endpoints for frontend integration
- [cite_start]`apps/web` — client-facing server-rendered reservation forms and calendar [cite: 12, 13, 22]

## Important project conventions

- [cite_start]Put table-assignment and capacity verification logic in `services.py`, not in views or serializers[cite: 15, 23].
- [cite_start]Put reusable availability and booking query logic in `selectors.py`[cite: 20].
- Keep background tasks thin; they should call service functions.

## Commands

- Run server: `python manage.py runserver`
- Run tests and check coverage: `uv run pytest`
- Lint and format code: `uv run ruff check` / `uv run ruff format`
- Create migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`

## Things that are easy to break

- [cite_start]Double-booking validation logic in `apps/reservations/services.py` [cite: 15, 23]
- [cite_start]Alternative timeslot suggestion logic when fully booked [cite: 16]
- [cite_start]API response shapes for calendar and seat availability data [cite: 13, 20]

## Change coupling

If you change:
- [cite_start]a model (e.g., restaurant_tables or reservations) → also check serializers, factories, and admin [cite: 5, 7, 9]
- [cite_start]reservation workflow → also check status transitions and notification tasks [cite: 18]
- [cite_start]user capacities → also check availability calculation queries [cite: 20]

## Constraints

- Do not edit old migrations; create a new one instead.
- Do not rename API fields or URL names unless explicitly asked.
- Prefer small, targeted changes over broad refactors.

## Documentation use

- [cite_start]Use `openspec/specs/*` as the canonical source for technical/runtime documentation[cite: 175, 177].
- For project-level conventions, examine the `context` section of `openspec/config.yaml`.
- [cite_start]For system-specific tasks, read the relevant capability spec under `openspec/specs/<capability>/spec.md` (for example: `reservation-workflow`, `user-management`)[cite: 175].
- [cite_start]Use `openspec/notes/*` as supplemental context only for non-normative ideas and backlog notes[cite: 177, 187].
- [cite_start]Keep technical/runtime truth in `openspec/specs/*`; promote accepted ideas from notes into specs[cite: 175, 187].
- Keep documentation up to date. [cite_start]If inconsistency between code and documentation is detected, report it to the user and suggest a fix[cite: 175].
- [cite_start]When a new feature is implemented or a certain fact about the system is discovered, suggest reflecting it in documentation[cite: 175].

## Testing expectations

Add or update tests for:
- [cite_start]Table booking availability validation (preventing double-bookings) [cite: 15, 23]
- [cite_start]Alternative timeslot auto-suggestions [cite: 16]
- [cite_start]Reservation database storage records and API shapes [cite: 18, 20]