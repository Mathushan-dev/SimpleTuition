from fastapi import FastAPI
from routes import user_routes, booking_routes, auth_routes  # Your routers
from routes import admin_routes
from models import mongo as mongo_db
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI()

# Simple session secret for dev; in production set SECRET_KEY env var
secret = os.environ.get("SECRET_KEY", "dev-secret-change-me")
# Harden session cookie settings: use secure flags in production via env
session_cookie = os.environ.get("SESSION_COOKIE_NAME", "session")
session_max_age = int(os.environ.get("SESSION_MAX_AGE", 14 * 24 * 3600))
session_same_site = os.environ.get("SESSION_SAME_SITE", "lax")
https_only = os.environ.get("SESSION_HTTPS_ONLY", "false").lower() in ("1", "true", "yes")
app.add_middleware(SessionMiddleware, secret_key=secret, session_cookie=session_cookie, max_age=session_max_age, same_site=session_same_site, https_only=https_only)

# Register your routes
app.include_router(user_routes.router)
app.include_router(booking_routes.router)
app.include_router(auth_routes.router)
app.include_router(admin_routes.router)


@app.on_event("startup")
def on_startup():
    ok = mongo_db.init_mongo()
    if not ok:
        raise RuntimeError("MongoDB connection failed. Ensure MONGODB_URI is set and the server is running.")
    app.state.db_backend = 'mongodb'
    print(f"Database backend: {app.state.db_backend}")

# Set up HTML templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
