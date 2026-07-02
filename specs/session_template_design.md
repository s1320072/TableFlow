# Session & Template Design for TableFlow

## 1. State Handling: Database vs Session

### 1.1 Current State

| Data | Where Stored | Notes |
|---|---|---|
| `Table` records | Database (`Table` model) | table_number, capacity, is_active |
| `Reservation` records | Database (`Reservation` model) | customer_name, num_guests, reservation_time, table FK, status |
| Reservation form input | Nowhere (lost on page load) | POST body forwarded to confirmation template but never persisted |
| Multi-step wizard state | Not implemented | N/A |
| User auth state | DB (Django `auth.User`) + Django session | No custom account models yet |

### 1.2 Design Principle

**Persist authoritative data in the database; use the session only for ephemeral, user-scoped workflow state.**

### 1.3 Database (Persistent / Authoritative)

| Data | Rationale |
|---|---|
| `Table` records | Tables are domain entities that outlive any single user session. |
| `Reservation` records | Reservations are the core business object — they must survive server restarts and be queryable by staff, other users, and background tasks. |
| `User` / account data | Authentication and role data must be durable and shared across all future sessions. |

### 1.4 Session (Ephemeral / Workflow-Scoped)

The session is not used at all today. Introduce it only for the following **multi-step or transient** use cases:

| Data | Rationale |
|---|---|
| Multi-step reservation wizard progress | If the UX splits booking across N pages (e.g., Step 1: pick date/time, Step 2: pick table, Step 3: confirm), accumulate state in the session and flush to DB only on the final commit. |
| "Flash" messages (success/error notifications) | One-shot messages that cross a redirect — use Django's `messages` framework (backed by session). |
| Guest reservation draft (unauthenticated user) | If an anonymous user builds a reservation over multiple steps, store the draft in the session until they authenticate or the session expires. |
| Recently viewed / suggested alt-time slots | Read from the reservation availability selector but cached in session so the user sees them as a hint when they reload the form. |

### 1.5 Rules of Thumb

1. **If it must survive a server restart, put it in the DB.** Everything else is a candidate for the session.
2. **Never store business-authoritative state in the session.** The session is per-user, easily lost, and not queryable by other parts of the system.
3. **Keep session keys small and namespaced** (e.g., `reservation_wizard`, `flash_alt_slots`).
4. **Clear session keys as soon as the workflow completes** to avoid stale data leaking into future requests.
5. **Use Django's `messages` framework** for one-shot notifications instead of raw `request.session` manipulation.

## 2. Template Inheritance Structure

### 2.1 Problem

All four existing templates (`home.html`, `list.html`, `form.html`, `confirmation.html`) duplicate the full HTML boilerplate (`<!DOCTYPE html>`, `<head>`, navigation links). There is no shared layout.

### 2.2 Proposed `base.html` Structure

```
apps/reservations/templates/reservations/
  base.html          ← NEW: shared skeleton
  home.html          ← extends base.html
  list.html          ← extends base.html
  form.html          ← extends base.html
  confirmation.html  ← extends base.html
```

#### `base.html` — Skeleton Template

```django
<!DOCTYPE html>
{% load static %}
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}TableFlow{% endblock %}</title>
  {% block extra_head %}{% endblock %}
</head>
<body>
  <header>
    <nav>
      <a href="{% url 'home' %}">Home</a>
      <a href="{% url 'reservation-list' %}">Reservations</a>
      <a href="{% url 'reservation-form' %}">New Reservation</a>
    </nav>
    {% block breadcrumb %}{% endblock %}
  </header>

  <main>
    {% block content %}
    {% endblock %}
  </main>

  <footer>
    <p>&copy; TableFlow</p>
  </footer>
</body>
</html>
```

**Block inventory:**

| Block | Purpose | Override in... |
|---|---|---|
| `title` | Page-specific `<title>` suffix | All child templates |
| `extra_head` | Per-page CSS / meta tags | Any page that needs custom head content |
| `breadcrumb` | Optional breadcrumb trail | Could be used by form/confirmation |
| `content` | **Primary** — main page body | **All child templates** (required) |

### 2.3 Child Template Examples

#### `home.html`
```django
{% extends "reservations/base.html" %}
{% block title %}TableFlow - Home{% endblock %}
{% block content %}
<h1>Welcome to TableFlow</h1>
<p>Server time: {{ now }}</p>
{% endblock %}
```

#### `list.html`
```django
{% extends "reservations/base.html" %}
{% block title %}Reservations{% endblock %}
{% block content %}
<h1>Reservations</h1>
<ul>
{% for r in reservations %}
  <li>…</li>
{% empty %}
  <li>No reservations.</li>
{% endfor %}
</ul>
{% endblock %}
```

#### `form.html`
```django
{% extends "reservations/base.html" %}
{% block title %}New Reservation{% endblock %}
{% block content %}
<h1>New Reservation</h1>
<form method="post" action="{% url 'process-reservation' %}">
  {% csrf_token %}
  …
</form>
{% endblock %}
```

#### `confirmation.html`
```django
{% extends "reservations/base.html" %}
{% block title %}Confirmation{% endblock %}
{% block content %}
<h1>Reservation Submitted (Stub)</h1>
…
{% endblock %}
```

### 2.4 Benefits

- **DRY**: Navigation links, `<head>`, and wrapper markup live in one place.
- **Consistent branding**: Changing the site header or adding CSS affects every page via a single edit.
- **Gradual migration**: Each child template can be converted independently; there is no need to do all at once.
- **Future-proof**: Adding new pages (e.g., login, dashboard) is trivial — just extend `base.html` and fill `content`.

### 2.5 Future Extensions (Deferred)

- Add a `{% block sidebar %}` for pages that need a side panel (e.g., admin dashboard).
- Add a `{% block scripts %}` at the bottom of `<body>` for per-page JavaScript (today there is none).
- Introduce a CSS framework (e.g., Bootstrap) by linking it in `base.html`; individual pages remain framework-agnostic.
