# Software Requirements Specification (SRS)
## Event Management System (Django Mini Project)

**Version:** 1.0
**Prepared for:** Python Django Basics Workshop
**Tech Stack:** Django (FBV), SQLite, Bootstrap, jQuery

---

## 1. Introduction

### 1.1 Purpose
This document describes the requirements for a simple **Event Management System** built as a practice project for workshop attendees. The goal is to apply Function-Based Views (FBV), the PRG (Post-Redirect-Get) pattern, Django Forms, and email sending in a small, realistic app.

### 1.2 Scope
Users can register/login, create events, join events, and cancel their seat. A visual seat map shows how many seats are booked vs available for each event. This is a mock project — no payments, no complex roles, no production security hardening.

### 1.3 Intended Audience
Workshop students building their first end-to-end Django app.

---

## 2. General Description

### 2.1 User Types
- **Guest** – not logged in; can view event list, cannot join.
- **Registered User** – can log in, create events, join/cancel seats.
- *(No separate "admin" role needed — any logged-in user can create events, keeping scope simple.)*

### 2.2 Assumptions & Constraints
- Single Django app, FBVs only (no CBVs, no DRF/API).
- SQLite database (default).
- No payment gateway — joining an event is free.
- Email sending uses Django's console/SMTP backend (e.g., confirmation email on join).
- Bootstrap 5 for styling; jQuery for small interactions (e.g., confirm dialogs, dynamic seat highlight).

---

## 3. Functional Requirements

### FR1 – User Registration
- Form fields: Name, Username, Email, Password, Confirm Password.
- On success: save user, redirect to Login page (PRG).
- On failure: re-render form with errors.

### FR2 – User Login / Logout
- Standard Django auth (`authenticate`, `login`, `logout`).
- Redirect to Event List after login/logout (PRG).
- Navbar shows Login/Register (guest) or Username/Logout (logged in).

### FR3 – Create Event
- Only for logged-in users.
- Form fields: Event Name, Description, Date & Time, Venue, Total Seats.
- On submit: save event with `organizer = request.user`, redirect to Event List.
- Use Django Forms with validation (e.g., total seats > 0, date must be in future).

### FR4 – Event List Page
- Shows all upcoming events as cards/table: Name, Date, Venue, Seats Available/Total.
- "View Details" button per event.

### FR5 – Event Detail Page
- Shows full event info + **Seat Occupancy UI** (see Section 4).
- "Join Event" button (disabled/hidden if user already joined, or seats full).
- "Cancel My Seat" button (visible only if user has joined).

### FR6 – Join Event
- Logged-in users only (redirect to login if not).
- Checks: seat availability, user not already registered for this event.
- On success: create a Booking record, decrement available seats, send confirmation email, redirect back to Event Detail (PRG).
- On failure (event full / already joined): show message, redirect back.

### FR7 – Cancel Seat
- Only for the user who booked it.
- Deletes Booking record, increments available seat count.
- Optional: send cancellation email.
- Redirect back to Event Detail (PRG).

### FR8 – Email Notifications
- Send email on:
  - Successful join (booking confirmation with event details).
  - (Optional) Seat cancellation.
- Use Django's `send_mail()`; console backend for local testing.

### FR9 – My Events / My Bookings (optional stretch goal)
- Page listing events the user created, and events the user has joined.

---

## 4. Seat Occupancy UI (Key Feature)

- Event Detail page displays seats as a **grid of numbered boxes** (like a mini theatre seat map) or a **progress-bar table**, e.g.:
  - Booked seat → filled/colored box (Bootstrap `bg-danger` / `bg-success`).
  - Available seat → outlined box.
  - Simple legend: Available (green), Booked (red).
- Alternative simpler version: Bootstrap **progress bar** showing `X / Total seats booked`, plus a small table listing attendee names.
- jQuery used to:
  - Show a confirm dialog before Join/Cancel (`.click()` + `confirm()` or a Bootstrap modal).
  - Animate/update the progress bar or seat highlight without extra styling logic in the template.

*(Keep implementation simple: seat numbers don't need to map to real booking identities — just represent count visually.)*

---

## 5. Data Model (Suggested)

**Event**
- id, name, description, date_time, venue, total_seats, organizer (FK → User), created_at

**Booking**
- id, event (FK → Event), user (FK → User), booked_at
- (unique_together: event + user → prevents double booking)

*Available seats = `total_seats - Booking.objects.filter(event=event).count()`*

---

## 6. Non-Functional Requirements

| Category | Requirement |
|---|---|
| Usability | Clean, responsive UI using Bootstrap; mobile-friendly cards/tables |
| Performance | Not a concern for this mock project (small dataset) |
| Security | Basic Django auth; CSRF tokens on all forms; login_required decorators |
| Maintainability | Simple FBV structure: `views.py`, `forms.py`, `models.py`, `urls.py` |
| Portability | Runs locally via `manage.py runserver`; SQLite, no external services required |

---

## 7. Page / URL Summary

| Page | URL | Auth Required |
|---|---|---|
| Event List (Home) | `/` | No |
| Register | `/register/` | No |
| Login | `/login/` | No |
| Logout | `/logout/` | Yes |
| Create Event | `/event/create/` | Yes |
| Event Detail | `/event/<id>/` | No (Join needs login) |
| Join Event | `/event/<id>/join/` | Yes |
| Cancel Seat | `/event/<id>/cancel/` | Yes |

---

## 8. Django Concepts Mapped to Features

| Concept Learned | Applied In |
|---|---|
| FBV | All views |
| PRG Cycle | Register, Login, Create Event, Join, Cancel |
| Django Forms | Registration, Login, Create Event |
| Mail Sending | Booking confirmation email |
| Bootstrap + jQuery | Navbar, cards, seat grid, confirm modals |

---

## 9. Out of Scope
- Payments / paid tickets
- Event categories, search, or filters
- Admin dashboard / analytics
- Waitlists for full events
- Password reset via email

---

*End of SRS.*
