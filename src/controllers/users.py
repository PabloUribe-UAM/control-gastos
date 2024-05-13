from copy import copy
from typing import List
from fastapi import APIRouter, Body, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..config.database import SessionLocal
from ..models.users import User
from ..schemas.User import UserSchema
from ..utils.password import Password
import re as regex


router = APIRouter(prefix="/users")



@router.post('', description="Create a new user")
def create(user: UserSchema = Body()):
    db = SessionLocal()
    old = db.query(User).filter(User.id == user.id).first()
    if old is not None:
        return JSONResponse({
            "status": 400,
            "message": "User already exists"
        }, 400)
    old = db.query(User).filter(User.email == user.email).first()
    if old is not None:
        return JSONResponse({
            "status": 400,
            "message": "Email already used"
        }, 400)
    new_user = User(**user.model_dump())
    new_user.password = Password.hash(new_user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse({
        "status": 201,
        "message": "User created",
        "user": jsonable_encoder(new_user)
    }, 201)

@router.get('', description="List all users")
def get_all(active: str | None = Query(None), email: str | None = Query(None)):
    db = SessionLocal()
    user_filter = db.query(User)
    if active is not None:
        if not regex.match(r'^((true)|(false))$', active):
            return JSONResponse({
                "status": 400,
                "message": f"Not recognized value '{active}'"
            }, 400)
        user_filter = user_filter.filter(User.active == (active=="true") )
    if email is not None:
        if not regex.match(r'^[a-z0-9!&\-#.~]+@[a-z0-9]+\.(([a-z0-9]+\.)+)?[a-z0-9]+$', email):
            return JSONResponse({
                "status": 400,
                "input": email,
                "message": f"Email format is not valid"
            }, 400)
        user_filter = user_filter.filter(User.email == email)

    return JSONResponse(jsonable_encoder(user_filter.all()), 200)

@router.get('/{id}', description="Get the info from a single user using the id")
def get_by_id(id: str = Path()):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        return JSONResponse({
            "status": 404,
            "message": "User not found"
        }, 404)
    return JSONResponse(jsonable_encoder(user), 200)

@router.put('/{id}', description="Update a user")
def update(id: str = Path(), payload: UserSchema = Body()):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()
    if user == None:
        return JSONResponse({
            "status": 404,
            "message": "User not found"
        }, 404)
    old = db.query(User).filter(User.email == payload.email).first()
    if old is not None and old.id != user.id:
        return JSONResponse({
            "status": 400,
            "message": "Email already used"
        }, 400)
    user.email = payload.email
    user.name = payload.name
    user.lastname = payload.lastname
    user.active = payload.active
    db.commit()
    db.refresh(user)
    return JSONResponse({
        "status": 200,
        "message": "User updated",
        "user": jsonable_encoder(user)
    }, 200)

@router.delete('/{id}', description="Remove an existent user")
def delete(id: str = Path()):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()
    if user == None:
        return JSONResponse({
            "status": 404,
            "message": "User not found"
        }, 404)
    db.delete(user)
    db.commit()
    return JSONResponse({
        "status": 200,
        "message": "User deleted",
        "user": jsonable_encoder(user)
    }, 200)