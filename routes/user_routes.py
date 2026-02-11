from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from models.user import UserCreate, UserResponse
from models.user import user as UserLogic
from models import mongo as mongo_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate):
    # If Mongo is configured, use it
    if mongo_db.find_user_by_id(user.user_id):
        raise HTTPException(status_code=400, detail="User ID already exists")
    if mongo_db.find_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    # Hash via UserLogic
    user_logic = UserLogic(user_id=user.user_id, name=user.name, email=user.email, password=user.password, user_type=user.user_type)
    doc = {"user_id": user_logic.user_id, "name": user_logic.name, "email": user_logic.email, "password": user_logic.password.decode() if isinstance(user_logic.password, bytes) else user_logic.password, "user_type": user_logic.user_type}
    mongo_db.create_user(doc)
    return {"user_id": user_logic.user_id, "name": user_logic.name, "email": user_logic.email, "user_type": user_logic.user_type}


def get_user_by_id(user_id: int):
    u = mongo_db.find_user_by_id(user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user_obj = get_user_by_id(user_id)
    # Support both dict (mongo) and ORM object
    if isinstance(user_obj, dict):
        return {"user_id": user_obj.get('user_id'), "name": user_obj.get('name'), "email": user_obj.get('email'), "user_type": user_obj.get('user_type')}
    return {"user_id": user_obj.user_id, "name": user_obj.name, "email": user_obj.email, "user_type": user_obj.user_type}


@router.get('/portal', response_model=None)
def portal_page(request: Request):
    return templates.TemplateResponse('portal.html', {'request': request})


@router.get('/subjects', response_model=None)
def subjects_page(request: Request):
    subjects = [mongo_db.serialize_subject(s) for s in mongo_db.db.subjects.find()]
    return templates.TemplateResponse('subjects.html', {'request': request, 'subjects': subjects})


@router.get('/about', response_model=None)
def about_page(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})


@router.get('/services', response_model=None)
def services_page(request: Request):
    return templates.TemplateResponse('services.html', {'request': request})


@router.get('/portfolio', response_model=None)
def portfolio_page(request: Request):
    return templates.TemplateResponse('portfolio.html', {'request': request})


@router.get('/contact', response_model=None)
def contact_page(request: Request):
    return templates.TemplateResponse('contact.html', {'request': request})


@router.post('/contact_submit')
def contact_submit(request: Request, name: str = Form(...), email: str = Form(...), subject: str = Form(None), message: str = Form(...)):
    # Simple dev-friendly contact handler: log to file and show thank you page
    try:
        with open('contact_submissions.txt', 'a') as f:
            f.write(f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}\n---\n")
    except Exception:
        pass
    return templates.TemplateResponse('contact_thanks.html', {'request': request, 'name': name})
