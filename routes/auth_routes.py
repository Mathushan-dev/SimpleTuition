from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import mongo as mongo_db
from datetime import datetime, timedelta
import secrets

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_user_by_email(email: str):
    from models.user import user as UserLogic
    m = mongo_db.find_user_by_email(email)
    if not m:
        return None
    pwd = m.get('password')
    if isinstance(pwd, str):
        pwd = pwd.encode()
    return UserLogic(user_id=m.get('user_id'), name=m.get('name'), email=m.get('email'), password=pwd, user_type=m.get('user_type'), password_is_hashed=True)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    # Public signup disabled — admins should create accounts
    return templates.TemplateResponse("signup.html", {"request": request, "error": "Signup is disabled. Ask an admin to create an account."})


@router.post("/signup")
def do_signup(request: Request, user_id: int = Form(...), name: str = Form(...), email: str = Form(...), password: str = Form(...), user_type: str = Form(...)):
    # Public signup is disabled; do not allow account creation via this endpoint.
    return templates.TemplateResponse("signup.html", {"request": request, "error": "Signup is disabled. Admins must create accounts."})


@router.post("/login")
def do_login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = get_user_by_email(email)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    if not user.check_password(password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

    # set server-side session
    request.session["user_id"] = int(user.user_id)
    request.session["user_type"] = user.user_type
    return RedirectResponse(url="/dashboard", status_code=303)


@router.get("/logout")
def logout(request: Request):
    # Clear server-side session and redirect to homepage
    try:
        request.session.clear()
    except Exception:
        pass
    response = RedirectResponse(url="/", status_code=303)
    return response


@router.get("/forgot_password", response_class=HTMLResponse)
def forgot_password_page(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request, "link": None})


@router.post("/forgot_password", response_class=HTMLResponse)
def forgot_password(request: Request, email: str = Form(...)):
    user = get_user_by_email(email)
    if not user:
        # return same template without revealing
        return templates.TemplateResponse("forgot_password.html", {"request": request, "link": None})

    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=1)
    # persist reset token
    mongo_db.create_reset_token({"token": token, "user_id": user.user_id, "expires_at": expires})

    link = f"/reset_password/{token}"
    # try to email; if SMTP not configured or send fails, show link for development convenience
    from utils.email_utils import send_reset_email
    sent = send_reset_email(user.email, request.url_for('reset_password_page', token=token))
    if sent:
        return templates.TemplateResponse("forgot_password.html", {"request": request, "link": None})
    return templates.TemplateResponse("forgot_password.html", {"request": request, "link": link})


@router.get("/reset_password/{token}", response_class=HTMLResponse)
def reset_password_page(request: Request, token: str):
    # check token in Mongo or SQL
    rt = mongo_db.find_reset_token(token)
    if not rt or (rt.get('expires_at') and rt.get('expires_at') < datetime.utcnow()):
        return templates.TemplateResponse("reset_password.html", {"request": request, "error": "Invalid or expired token", "token": token})
    return templates.TemplateResponse("reset_password.html", {"request": request, "error": None, "token": token})


@router.post("/reset_password/{token}")
def reset_password(request: Request, token: str, new_password: str = Form(...)):
    # Handle for Mongo or SQL
    from models.user import user as UserLogic
    rt = mongo_db.find_reset_token(token)
    if not rt or (rt.get('expires_at') and rt.get('expires_at') < datetime.utcnow()):
        return templates.TemplateResponse("reset_password.html", {"request": request, "error": "Invalid or expired token", "token": token})
    db_user = mongo_db.find_user_by_id(rt.get('user_id'))
    if not db_user:
        return templates.TemplateResponse("reset_password.html", {"request": request, "error": "User not found", "token": token})
    temp = UserLogic(user_id=db_user.get('user_id'), name=db_user.get('name'), email=db_user.get('email'), password=new_password, user_type=db_user.get('user_type'))
    mongo_db.db.users.update_one({"user_id": db_user.get('user_id')}, {"$set": {"password": temp.password.decode() if isinstance(temp.password, bytes) else temp.password}})
    mongo_db.delete_reset_token(token)
    return RedirectResponse(url="/login", status_code=303)


def get_current_user(request: Request):
    uid = request.session.get("user_id")
    if not uid:
        return None
    try:
        uid = int(uid)
    except ValueError:
        return None
    from models.user import user as UserLogic
    m = mongo_db.find_user_by_id(uid)
    if not m:
        return None
    pwd = m.get('password')
    if isinstance(pwd, str):
        pwd = pwd.encode()
    return UserLogic(user_id=m.get('user_id'), name=m.get('name'), email=m.get('email'), password=pwd, user_type=m.get('user_type'), password_is_hashed=True)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")

    # Student view (read-only)
    if user.user_type == "student":
        student_bookings = [mongo_db.serialize_booking(b) for b in mongo_db.db.bookings.find({"student_id": user.user_id})]
        return templates.TemplateResponse("dashboard_student.html", {"request": request, "user": user, "bookings": student_bookings})

    # Tutor view
    if user.user_type == "tutor":
        # tutor can see their classes and expected payments
        tutor_bookings = [mongo_db.serialize_booking(b) for b in mongo_db.db.bookings.find({"teacher_id": user.user_id})]
        # compute simple due amount: assume each booking has subject_id and fixed fee 20
        due = len([b for b in tutor_bookings if b.get('status') == 'confirmed']) * 20
        return templates.TemplateResponse("dashboard_tutor.html", {"request": request, "user": user, "bookings": tutor_bookings, "due": due})

    # Admin view
    return RedirectResponse(url="/admin", status_code=303)


@router.get("/bookings_page", response_class=HTMLResponse)
def bookings_page(request: Request):
    # Bookings page removed — redirect to dashboard
    return RedirectResponse(url='/', status_code=303)


@router.get("/lessons_page", response_class=HTMLResponse)
def lessons_page(request: Request):
    """New lessons page — same data as bookings but reworded for users."""
    user = get_current_user(request)
    bookings = [mongo_db.serialize_booking(b) for b in mongo_db.db.bookings.find()]
    users = [mongo_db.serialize_user(u) for u in mongo_db.db.users.find()]
    subjects = [mongo_db.serialize_subject(s) for s in mongo_db.db.subjects.find()]
    users_map = {int(u.get("user_id")): u.get("name") for u in users if u.get("user_id") is not None}
    subjects_map = {int(s.get("subject_id")): s.get("name") for s in subjects if s.get("subject_id") is not None}
    return templates.TemplateResponse("lessons.html", {"request": request, "bookings": bookings, "users": users, "subjects": subjects, "users_map": users_map, "subjects_map": subjects_map, "user": user})


@router.post("/create_booking")
def create_booking(request: Request, booking_id: int = Form(...), student_id: int = Form(...), teacher_id: int = Form(...), subject_id: int = Form(...), date_time: str = Form(...), status: str = Form("confirmed")):
    user = get_current_user(request)
    if not user or user.user_type not in ("tutor", "admin"):
        raise HTTPException(status_code=403, detail="Only tutors or admins can create bookings")

    try:
        # datetime-local yields 'YYYY-MM-DDTHH:MM'
        dt = datetime.fromisoformat(date_time)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date/time format")

    # conflict check
    existing = mongo_db.db.bookings.find_one({"teacher_id": teacher_id, "date_time": dt})
    if existing:
        raise HTTPException(status_code=400, detail="Time slot already booked for this tutor.")
    doc = {"booking_id": booking_id, "student_id": student_id, "teacher_id": teacher_id, "subject_id": subject_id, "date_time": dt, "status": status}
    mongo_db.create_booking(doc)
    return RedirectResponse(url="/bookings_page", status_code=303)


@router.get('/reschedule', response_class=HTMLResponse)
def reschedule_page(request: Request, booking_id: int = None):
    return templates.TemplateResponse('reschedule.html', {'request': request, 'error': None})


@router.post('/reschedule_action')
def reschedule_action(request: Request, booking_id: int = Form(...), date_time: str = Form(...)):
    user = get_current_user(request)
    if not user or user.user_type not in ('tutor', 'admin'):
        raise HTTPException(status_code=403, detail='Only tutors or admins can reschedule')
    try:
        dt = datetime.fromisoformat(date_time)
    except Exception:
        return templates.TemplateResponse('reschedule.html', {'request': request, 'error': 'Invalid date format'})
    # Update in Mongo or SQL
    res = mongo_db.db.bookings.update_one({'booking_id': booking_id}, {'$set': {'date_time': dt}})
    if res.matched_count == 0:
        return templates.TemplateResponse('reschedule.html', {'request': request, 'error': 'Lesson not found'})
    return RedirectResponse(url='/lessons_page', status_code=303)


# Tutor records attendance
@router.post("/record_attendance")
def record_attendance(request: Request, booking_id: int = Form(...), present: bool = Form(...)):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=403, detail="Not logged in")
    if user.user_type not in ("tutor", "admin"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    b = mongo_db.db.bookings.find_one({"booking_id": booking_id})
    if not b:
        raise HTTPException(status_code=404, detail="Booking not found")
    new_status = "attended" if present in (True, "true", "True", "1") else "absent"
    mongo_db.db.bookings.update_one({"booking_id": booking_id}, {"$set": {"status": new_status}})
    return {"message": "Attendance recorded"}


# Tutor/Teacher records a payment for a student
@router.post("/record_payment")
def record_payment(request: Request, booking_id: int = Form(...), amount: float = Form(...)):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=403, detail="Not logged in")
    if user.user_type not in ("tutor", "admin"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    b = mongo_db.db.bookings.find_one({"booking_id": booking_id})
    if not b:
        raise HTTPException(status_code=404, detail="Booking not found")
    note = f"Payment recorded: £{amount} by {user.name} on {datetime.utcnow().isoformat()}"
    existing = b.get('admin_notes') or ''
    new_notes = note if not existing else existing + ' | ' + note
    mongo_db.db.bookings.update_one({"booking_id": booking_id}, {"$set": {"admin_notes": new_notes}})
    return {"message": "Payment recorded"}


# Admin: add a user
@router.post("/admin/add_user")
def admin_add_user(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(None), user_type: str = Form(...)):
    user = get_current_user(request)
    if not user or user.user_type != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    # check duplicates
    if get_user_by_email(email):
        raise HTTPException(status_code=400, detail="Email exists")

    # generate a random, unique user_id for the new user
    import secrets
    def _exists_id(nid):
        return mongo_db.db.users.find_one({'user_id': nid}) is not None

    # create a random id in a large space and ensure uniqueness
    attempt = 0
    while True:
        nid = secrets.randbelow(900000) + 1000
        if not _exists_id(nid):
            user_id = nid
            break
        attempt += 1
        if attempt > 10:
            # fallback to sequential allocation if unlucky
            cur = list(mongo_db.db.users.find({}, {'user_id': 1}).sort('user_id', -1).limit(1))
            user_id = (cur[0].get('user_id') if cur and cur[0].get('user_id') else 1000) + 1
            break

    # generate a temporary password if not supplied
    import secrets
    temp_password = password or secrets.token_urlsafe(8)

    from models.user import user as UserLogic
    uobj = UserLogic(user_id=int(user_id), name=name, email=email, password=temp_password, user_type=user_type)

    doc = {"user_id": uobj.user_id, "name": uobj.name, "email": uobj.email, "password": uobj.password.decode() if isinstance(uobj.password, bytes) else uobj.password, "user_type": uobj.user_type}
    mongo_db.create_user(doc)
    # store created_user info in session so /admin can display it after redirect
    request.session['created_user'] = {"email": uobj.email, "password": temp_password, "user_id": uobj.user_id}
    return RedirectResponse(url="/admin", status_code=303)


# Admin: remove user by id
@router.post("/admin/remove_user")
def admin_remove_user(request: Request, user_id: int = Form(...)):
    user = get_current_user(request)
    if not user or user.user_type != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    mongo_db.db.users.delete_one({"user_id": user_id})
    return RedirectResponse(url="/admin", status_code=303)


@router.post("/change_password")
def change_password(request: Request, current_password: str = Form(...), new_password: str = Form(...)):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=403, detail="Not logged in")
    # verify current
    if not user.check_password(current_password):
        raise HTTPException(status_code=400, detail="Current password incorrect")
    user.change_password(new_password)
    mongo_db.db.users.update_one({"user_id": user.user_id}, {"$set": {"password": user.password.decode() if isinstance(user.password, bytes) else user.password}})
    return RedirectResponse(url="/dashboard", status_code=303)


@router.post("/admin/reset_password")
def admin_reset_password(request: Request, user_id: int = Form(...), new_password: str = Form(...)):
    user = get_current_user(request)
    if not user or user.user_type != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    from models.user import user as UserLogic
    db_user = mongo_db.find_user_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    temp = UserLogic(user_id=db_user.get('user_id'), name=db_user.get('name'), email=db_user.get('email'), password=new_password, user_type=db_user.get('user_type'))
    mongo_db.db.users.update_one({"user_id": user_id}, {"$set": {"password": temp.password.decode() if isinstance(temp.password, bytes) else temp.password}})
    return RedirectResponse(url="/admin", status_code=303)
