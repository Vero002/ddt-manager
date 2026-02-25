from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models
from app.auth import verify_password, create_access_token, get_password_hash

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# -----------------------
# DATABASE
# -----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------
# PAGINA LOGIN
# -----------------------
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# -----------------------
# LOGIN POST
# -----------------------
@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Username o password errati")

    access_token = create_access_token(data={"sub": user.username})

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)

    return response


# -----------------------
# LOGOUT
# -----------------------
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("access_token")
    return response