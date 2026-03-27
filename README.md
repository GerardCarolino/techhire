# TechHire — Premium Job Board API

A Django REST Framework API that powers a freemium developer job board.
Anyone can browse jobs, but **company name, salary, and application link are masked** behind a Premium membership.

---

## Tech Stack

| Layer | Library |
|---|---|
| Web framework | Django 4.2 |
| REST API | djangorestframework 3.15 |
| Authentication | djangorestframework-simplejwt 5.3 |
| Filtering | django-filter 23 |
| Database | SQLite (dev) / PostgreSQL (prod) |

---

## Project Structure

```
techhire/
├── manage.py
├── requirements.txt
├── TechHire_API.postman_collection.json
│
├── techhire/               # Django project config
│   ├── settings.py
│   └── urls.py
│
├── accounts/               # User registration + membership
│   ├── models.py           # UserProfile (basic / premium)
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
└── jobs/                   # Job board core
    ├── models.py           # JobPosting
    ├── serializers.py      # ← Field-level masking lives here
    ├── filters.py          # Search / filter / ordering
    ├── views.py
    ├── urls.py
    └── management/
        └── commands/
            └── seed_data.py
```

---

## Quick Start

```bash
# 1. Clone and enter the project
git clone https://github.com/YOUR_USERNAME/techhire.git
cd techhire

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Seed sample data (12 jobs + 2 test users)
python manage.py seed_data

# 6. (Optional) Create a superuser for /admin
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver
```

The API is now live at **http://127.0.0.1:8000**

---

## API Reference

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/token/` | Obtain JWT (access + refresh) |
| POST | `/api/auth/token/refresh/` | Refresh access token |
| POST | `/api/auth/token/verify/` | Verify a token |

**Login body:**
```json
{ "username": "premium_user", "password": "TestPass123!" }
```

**Response:**
```json
{ "access": "eyJ...", "refresh": "eyJ..." }
```

Use the access token in subsequent requests:
```
Authorization: Bearer eyJ...
```

---

### Accounts

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/accounts/register/` | None | Register new user |
| GET | `/api/accounts/me/` | Required | Get own profile |
| PATCH | `/api/accounts/upgrade/` | Required | Upgrade to Premium |

**Register body:**
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "SecurePass99!",
  "password2": "SecurePass99!",
  "membership_tier": "premium"
}
```

---

### Jobs

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/jobs/` | Optional | List all jobs (paginated) |
| GET | `/api/jobs/<id>/` | Optional | Retrieve single job |

#### Query Parameters

| Param | Example | Description |
|---|---|---|
| `search` | `?search=backend` | Full-text search on title + description |
| `location` | `?location=Remote` | Filter by location (case-insensitive) |
| `location_in` | `?location_in=Remote,New York` | Filter by multiple locations |
| `created_after` | `?created_after=2024-01-01` | Jobs posted after date |
| `created_before` | `?created_before=2024-12-31` | Jobs posted before date |
| `ordering` | `?ordering=-created_at` | Sort field (default: newest first) |
| `page` | `?page=2` | Page number (10 per page) |

---

## Field-Level Masking

This is the core feature of TechHire. The masking logic lives entirely in **`jobs/serializers.py`**.

### How It Works

`JobPostingSerializer.to_representation()` is called for every job object before it's sent to the client. It inspects the request context to determine the user's tier:

```
Request received
     │
     ▼
Is request.user authenticated?
     │
     ├── NO  → mask all 3 premium fields
     │
     └── YES → Does user.profile.is_premium == True?
                    │
                    ├── NO  → mask (Basic tier)
                    │
                    └── YES → return full data ✓
```

### Response Comparison

**Unauthenticated / Basic user:**
```json
{
  "id": 1,
  "title": "Senior Backend Engineer",
  "description": "We are looking for...",
  "location": "Remote",
  "company_name": "🔒 Premium Feature",
  "salary_range": "🔒 Premium Feature",
  "application_link": "🔒 Premium Feature",
  "created_at": "2024-11-01T10:00:00Z"
}
```

**Premium user:**
```json
{
  "id": 1,
  "title": "Senior Backend Engineer",
  "description": "We are looking for...",
  "location": "Remote",
  "company_name": "Stripe",
  "salary_range": "$160,000 – $210,000",
  "application_link": "https://stripe.com/jobs/senior-backend-engineer",
  "created_at": "2024-11-01T10:00:00Z"
}
```

---

## Test Credentials (after running `seed_data`)

| Username | Password | Tier | Fields |
|---|---|---|---|
| `basic_user` | `TestPass123!` | Basic | Masked |
| `premium_user` | `TestPass123!` | Premium | Revealed |

---

## Postman Collection

Import `TechHire_API.postman_collection.json` into Postman.

The collection includes:
1. **POST: Get JWT Token (Basic User)** — auto-saves token to `basic_token` variable
2. **POST: Get JWT Token (Premium User)** — auto-saves token to `premium_token` variable
3. **GET: Unauthenticated — Locked Fields** ← Deliverable #2
4. **GET: Authenticated as Premium — Full Data** ← Deliverable #3
5. **GET: Single Job Detail — Premium** ← Deliverable #4
6. Additional requests for search, filter, upgrade, and registration

Automated test scripts in the Tests tab verify masking and unmasking behaviour.

---

## Production Notes

- Replace `SECRET_KEY` in `settings.py` with an environment variable
- Switch `DATABASES` to PostgreSQL
- Set `DEBUG = False` and configure `ALLOWED_HOSTS`
- The `/api/accounts/upgrade/` endpoint should be gated behind a real payment provider (Stripe, etc.)
