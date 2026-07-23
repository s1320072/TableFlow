# TableFlow: A Smart Restaurant Reservation System

## Project Outline
TableFlow is a web application designed for a fancy restaurant that automates table bookings. It dynamically assigns the most suitable table based on the number of guests and suggests alternative timeslots when the desired slot is fully booked.

## Development Environment
- Language: Python
- Virtual Environment & Package Manager: `uv`

## Tools Used
- **Linting & Formatting**: `ruff`
- **Testing**: `pytest`
- **Test Coverage**: `pytest-cov`

## Getting Started
To set up the development environment, ensure you have `uv` installed, then run:
```bash
uv venv
uv sync
```

## Deployment
To deploy the application in production:

1. **Collect static files:**
```bash
uv run python manage.py collectstatic --noinput
```

2. **Run the server with Waitress:**
```bash
uv run waitress-serve --host=0.0.0.0 --port=8000 config.wsgi:application
```