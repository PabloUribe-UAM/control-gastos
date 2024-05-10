from copy import copy
from typing import List
from fastapi import APIRouter, Body, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..config.database import SessionLocal
from ..models.users import User
from ..schemas.User import UserSchema
import re as regex


router = APIRouter(prefix="/users")



@router.post('', description="Create a new user")
def create(user: UserSchema = Body()):
    db = SessionLocal()
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    return JSONResponse({
        "status": 201,
        "message": "User created",
        "user": user.model_dump()
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