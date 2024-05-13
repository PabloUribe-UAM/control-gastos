from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.models.users import User
from src.config.database import SessionLocal
from src.utils.password import Password
from src.utils.jwt import JWT
from src.schemas.User import RegisterUserSchema, LoginUserSchema


router = APIRouter(prefix="/auth")
@router.post('/login')
def handle_login(payload: LoginUserSchema = Body()):
    db = SessionLocal()
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        return JSONResponse({
            "status": 401,
            "message": "Username or password incorrect"
        }, 401)
    if (not Password.compare(payload.password, user.password)):
        return JSONResponse({
            "status": 401,
            "message": "Username or password incorrect"
        }, 401)
    to_encode = jsonable_encoder(user)
    del to_encode['password']
    encoded = JWT.encode(to_encode, 60)
    return JSONResponse({
        "status": 200,
        "token": encoded
    }, 401)


@router.post('/register')
def handle_register(payload:RegisterUserSchema = Body()):
    db = SessionLocal()
    old = db.query(User).filter(User.id == payload.id).first()
    if old is not None:
        return JSONResponse({
            "status": 400,
            "message": "User already exists"
        }, 400)
    old = db.query(User).filter(User.email == payload.email).first()
    if old is not None:
        return JSONResponse({
            "status": 400,
            "message": "Email already used"
        }, 400)
    new_user = User(**payload.model_dump())
    new_user.password = Password.hash(new_user.password)
    new_user.active = True
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse({
        "status": 201,
        "message": "User created",
        "user": jsonable_encoder(new_user)
    }, 201)