from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from routes.auth_routes import get_current_user
from fastapi.templating import Jinja2Templates
from models import mongo as mongo_db
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/admin/users")
def admin_users(request: Request):
    cur = get_current_user(request)
    if not cur or cur.user_type != 'admin':
        raise HTTPException(status_code=403, detail='Admin only')
    users = [mongo_db.serialize_user(u) for u in mongo_db.db.users.find()]
    return templates.TemplateResponse("admin_users.html", {"request": request, "user": cur, "users": users, "created_user": None})


@router.get("/admin/lessons")
def admin_lessons(request: Request):
    cur = get_current_user(request)
    if not cur or cur.user_type != 'admin':
        raise HTTPException(status_code=403, detail='Admin only')
    bookings = [mongo_db.serialize_booking(b) for b in mongo_db.db.bookings.find()]
    return templates.TemplateResponse("admin_lessons.html", {"request": request, "user": cur, "bookings": bookings})


@router.get('/admin/edit_user', response_model=None)
def edit_user_page(request: Request, user_id: int = None):
    if not request.session.get('user_type') == 'admin':
        raise HTTPException(status_code=403, detail='Admin only')
    if user_id is None:
        return templates.TemplateResponse('admin_edit_user.html', {'request': request, 'user_obj': None, 'error': 'No user specified'})
    u = mongo_db.find_user_by_id(user_id)
    return templates.TemplateResponse('admin_edit_user.html', {'request': request, 'user_obj': u, 'error': None})


@router.post('/admin/edit_user')
def edit_user_action(request: Request, user_id: int = Form(...), name: str = Form(...), email: str = Form(...), user_type: str = Form(...)):
    if not request.session.get('user_type') == 'admin':
        raise HTTPException(status_code=403, detail='Admin only')
    res = mongo_db.db.users.update_one({'user_id': user_id}, {'$set': {'name': name, 'email': email, 'user_type': user_type}})
    return RedirectResponse(url='/admin/users', status_code=303)


@router.get('/admin/edit_lesson')
def edit_lesson_page(request: Request, booking_id: int = None):
    if not request.session.get('user_type') == 'admin':
        raise HTTPException(status_code=403, detail='Admin only')
    if booking_id is None:
        return templates.TemplateResponse('admin_edit_lesson.html', {'request': request, 'booking': None, 'error': 'No lesson specified'})
    b = mongo_db.db.bookings.find_one({'booking_id': booking_id})
    return templates.TemplateResponse('admin_edit_lesson.html', {'request': request, 'booking': b, 'error': None})


@router.post('/admin/edit_lesson')
def edit_lesson_action(request: Request, booking_id: int = Form(...), student_id: int = Form(...), teacher_id: int = Form(...), date_time: str = Form(...), status: str = Form(...)):
    if not request.session.get('user_type') == 'admin':
        raise HTTPException(status_code=403, detail='Admin only')
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(date_time)
    except Exception:
        raise HTTPException(status_code=400, detail='Invalid date format')
    res = mongo_db.db.bookings.update_one({'booking_id': booking_id}, {'$set': {'student_id': student_id, 'teacher_id': teacher_id, 'date_time': dt, 'status': status}})
    return RedirectResponse(url='/admin/lessons', status_code=303)


@router.get('/admin/subjects')
def admin_list_subjects(request: Request):
    cur = get_current_user(request)
    if not cur or cur.user_type != 'admin':
        raise HTTPException(status_code=403, detail='Admin only')
    subjects = [mongo_db.serialize_subject(s) for s in mongo_db.db.subjects.find()]
    assignments = mongo_db.list_subject_assignments()
    return templates.TemplateResponse('admin_subjects.html', {'request': request, 'user': cur, 'subjects': subjects, 'assignments': assignments})


@router.post('/admin/seed_subjects')
def admin_seed_subjects(request: Request):
    cur = get_current_user(request)
    if not cur or cur.user_type != 'admin':
        raise HTTPException(status_code=403, detail='Admin only')
    # Seeding subjects is disabled in production-ready mode.
    # Keep route to avoid 404 for older links, but do nothing.
    return RedirectResponse(url='/admin/subjects', status_code=303)



@router.post('/admin/subjects/assign')
def admin_assign_student(request: Request, subject_id: int = Form(...), student_id: int = Form(...), price: float = Form(None)):
    cur = get_current_user(request)
    if not cur or cur.user_type != 'admin':
        raise HTTPException(status_code=403, detail='Admin only')
    doc = {'subject_id': subject_id, 'student_id': student_id}
    if price is not None:
        doc['price'] = price
    mongo_db.assign_student_to_subject(doc)
    return RedirectResponse(url='/admin/assignments', status_code=303)


@router.post('/admin/subjects/set_price')
def admin_set_student_price(request: Request, subject_id: int = Form(...), student_id: int = Form(...), price: float = Form(...)):
    cur = get_current_user(request)
    if not cur or cur.user_type != 'admin':
        raise HTTPException(status_code=403, detail='Admin only')
    mongo_db.set_student_price(subject_id, student_id, price)
    return RedirectResponse(url='/admin/assignments', status_code=303)


@router.get('/admin/reports')
def admin_reports(request: Request):
    cur = get_current_user(request)
    if not cur or cur.user_type != 'admin':
        raise HTTPException(status_code=403, detail='Admin only')

    users = list(mongo_db.db.users.find())
    bookings = list(mongo_db.db.bookings.find())
    subjects = list(mongo_db.db.subjects.find())
    payments = list(mongo_db.db.tutor_payments.find())

    user_counts = {
        "students": len([u for u in users if u.get("user_type") == "student"]),
        "tutors": len([u for u in users if u.get("user_type") == "tutor"]),
        "admins": len([u for u in users if u.get("user_type") == "admin"]),
    }
    booking_counts = {
        "confirmed": len([b for b in bookings if b.get("status") == "confirmed"]),
        "pending": len([b for b in bookings if b.get("status") == "pending"]),
        "attended": len([b for b in bookings if b.get("status") == "attended"]),
        "absent": len([b for b in bookings if b.get("status") == "absent"]),
        "cancelled": len([b for b in bookings if b.get("status") == "cancelled"]),
    }

    upcoming = []
    now = datetime.utcnow()
    for b in bookings:
        dt = b.get("date_time")
        if isinstance(dt, str):
            try:
                dt = datetime.fromisoformat(dt)
            except ValueError:
                dt = None
        if isinstance(dt, datetime) and dt >= now:
            upcoming.append(b)
    upcoming = sorted(upcoming, key=lambda x: x.get("date_time"))[:8]

    total_payouts = sum([p.get("amount", 0) or 0 for p in payments])

    return templates.TemplateResponse(
        'admin_reports.html',
        {
            'request': request,
            'user': cur,
            'user_counts': user_counts,
            'booking_counts': booking_counts,
            'subjects': [mongo_db.serialize_subject(s) for s in subjects],
            'upcoming': [mongo_db.serialize_booking(b) for b in upcoming],
            'total_payouts': total_payouts,
        },
    )


@router.get('/admin/assignments')
def admin_assignments_page(request: Request):
    cur = get_current_user(request)
    if not cur or cur.user_type != 'admin':
        raise HTTPException(status_code=403, detail='Admin only')
    assignments = mongo_db.list_subject_assignments()
    # enrich assignments with student names for display
    enriched = []
    for a in assignments:
        try:
            student = mongo_db.find_user_by_id(a.get('student_id'))
            student_name = student.get('name') if student else None
        except Exception:
            student_name = None
        ea = dict(a)
        ea['student_name'] = student_name
        enriched.append(ea)
    return templates.TemplateResponse('admin_assignments.html', {'request': request, 'user': cur, 'assignments': enriched})



@router.get('/admin/edit_assignment')
def edit_assignment_page(request: Request, subject_id: int = None, student_id: int = None):
    if not request.session.get('user_type') == 'admin':
        raise HTTPException(status_code=403, detail='Admin only')
    if subject_id is None or student_id is None:
        return templates.TemplateResponse('admin_edit_assignment.html', {'request': request, 'assignment': None, 'student': None, 'subject': None, 'error': 'Missing subject_id or student_id'})
    a = mongo_db.db.subject_assignments.find_one({'subject_id': subject_id, 'student_id': student_id})
    if not a:
        return templates.TemplateResponse('admin_edit_assignment.html', {'request': request, 'assignment': None, 'student': None, 'subject': None, 'error': 'Assignment not found'})
    student = mongo_db.find_user_by_id(student_id)
    subject = mongo_db.db.subjects.find_one({'subject_id': subject_id})
    return templates.TemplateResponse('admin_edit_assignment.html', {'request': request, 'assignment': a, 'student': student, 'subject': subject, 'error': None})


@router.post('/admin/edit_assignment')
def edit_assignment_action(request: Request, subject_id: int = Form(...), student_id: int = Form(...), price: float = Form(None), remove: int = Form(None)):
    if not request.session.get('user_type') == 'admin':
        raise HTTPException(status_code=403, detail='Admin only')
    if remove:
        mongo_db.db.subject_assignments.delete_one({'subject_id': subject_id, 'student_id': student_id})
        return RedirectResponse(url='/admin/assignments', status_code=303)
    # update price (allow null to mean unset)
    if price is None or price == '':
        # remove price field
        mongo_db.db.subject_assignments.update_one({'subject_id': subject_id, 'student_id': student_id}, {'$unset': {'price': ''}})
    else:
        mongo_db.set_student_price(subject_id, student_id, price)
    return RedirectResponse(url='/admin/assignments', status_code=303)


@router.get('/admin')
def admin_dashboard(request: Request):
    cur = get_current_user(request)
    if not cur or cur.user_type != 'admin':
        raise HTTPException(status_code=403, detail='Admin only')

    users = [mongo_db.serialize_user(u) for u in mongo_db.db.users.find()]
    bookings = [mongo_db.serialize_booking(b) for b in mongo_db.db.bookings.find()]
    subjects = [mongo_db.serialize_subject(s) for s in mongo_db.db.subjects.find()]
    assignments = mongo_db.list_subject_assignments()

    # Reports data
    user_counts = {
        "students": len([u for u in users if u.get('user_type') == 'student']),
        "tutors": len([u for u in users if u.get('user_type') == 'tutor']),
        "admins": len([u for u in users if u.get('user_type') == 'admin']),
    }
    booking_counts = {
        "confirmed": len([b for b in bookings if b.get('status') == 'confirmed']),
        "pending": len([b for b in bookings if b.get('status') == 'pending']),
        "attended": len([b for b in bookings if b.get('status') == 'attended']),
        "absent": len([b for b in bookings if b.get('status') == 'absent']),
        "cancelled": len([b for b in bookings if b.get('status') == 'cancelled']),
    }
    payments = list(mongo_db.db.tutor_payments.find())
    total_payouts = sum([p.get('amount', 0) or 0 for p in payments])

    # upcoming
    now = datetime.utcnow()
    upcoming = []
    for b in bookings:
        dt = b.get("date_time")
        if isinstance(dt, str):
            try:
                dt = datetime.fromisoformat(dt)
            except Exception:
                dt = None
        if isinstance(dt, datetime) and dt >= now:
            upcoming.append(b)
    upcoming = sorted(upcoming, key=lambda x: x.get("date_time"))[:8]

    # Pop any created_user stored in session by admin actions
    created_user = None
    try:
        created_user = request.session.pop('created_user', None)
    except Exception:
        created_user = None

    return templates.TemplateResponse('dashboard_admin.html', {
        'request': request,
        'user': cur,
        'users': users,
        'bookings': bookings,
        'subjects': subjects,
        'assignments': assignments,
        'user_counts': user_counts,
        'booking_counts': booking_counts,
        'upcoming': upcoming,
        'total_payouts': total_payouts,
        'created_user': created_user,
    })
