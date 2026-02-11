# Tuition Centre Booking System

This project is a small FastAPI-based tuition centre booking system backed by MongoDB. It includes role-based user types (student, tutor, admin), booking management, basic payments/attendance recording, and a web UI.

Quick start (development):

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure MongoDB is running locally (or set `MONGODB_URI` to your hosted instance).

4. Run the app:

```bash
uvicorn main:app --reload
```

4. Open browser: http://127.0.0.1:8000/

Notes and production guidance:
- The app uses MongoDB via `pymongo`. Set `MONGODB_URI` (or `DATABASE_URL`) and `MONGODB_DB`.
- Sessions use Starlette `SessionMiddleware` with an environment `SECRET_KEY`; set a secure secret in production.
- The password reset flow displays reset links for development. Integrate an email provider for real deliveries.
- Add proper logging, monitoring and backup for production.
 
Production checklist
- Configure environment variables: `SECRET_KEY`, `MONGODB_URI`, `MONGODB_DB`, and SMTP settings (`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `FROM_EMAIL`).
- Use HTTPS and set `SESSION_HTTPS_ONLY=true` to enable secure cookies for sessions.
- Use a managed MongoDB deployment.
- Configure an SMTP provider (SendGrid, Mailgun, SES) for password reset emails.
- Add proper logging, monitoring and backup for production.

Simple container / PaaS instructions

- Build Docker image locally:

```bash
docker build -t tuition-app:latest .
docker run -p 8000:8000 --env SECRET_KEY="your-secret" tuition-app:latest
```

- Deploy to a simple PaaS (Heroku/Render): the included `Procfile` runs the app with `uvicorn`.

Set environment variables (`SECRET_KEY`, `MONGODB_URI`, `MONGODB_DB`, `SESSION_HTTPS_ONLY=true` in production) before starting.

# TuitionCentreBookingSystem
