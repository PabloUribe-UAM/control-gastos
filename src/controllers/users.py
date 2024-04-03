from copy import copy
from typing import List
from fastapi import APIRouter, Body, Path, Query
from fastapi.responses import JSONResponse
from ..localstorage.users import users
from ..models.User import User
import re as regex


router = APIRouter(prefix="/users")



@router.post('', description="Create a new user")
def create(user: User = Body()):
    users.append(user.model_dump())
    return JSONResponse({
        "status": 201,
        "message": "User created",
        "user": user.model_dump()
    }, 201)

@router.get('', description="List all users")
def get_all(status: str | None = Query(None), email: str | None = Query(None)):
    user_filter: List[User] = copy(users)
    if status is not None:
        if not regex.match(r'^((active)|(inactive))$', status):
            return JSONResponse({
                "status": 400,
                "message": f"Not recognized value '{status}'"
            }, 400)
        user_filter = [elem for elem in user_filter if elem['status'] == status]
    if email is not None:
        if not regex.match(r'^[a-z0-9!&\-#.~]+@[a-z0-9]+\.(([a-z0-9]+\.)+)?[a-z0-9]+$', email):
            return JSONResponse({
                "status": 400,
                "input": email,
                "message": f"Email format is not valid"
            }, 400)
        user_filter = [elem for elem in user_filter if elem['email'] == email]

    return JSONResponse(user_filter, 200)

@router.get('/{id}', description="Get the info from a single user using the id")
def get_by_id(id: str = Path()):
    user: User | None = None
    if len(users) == 0:
        return JSONResponse({
            "status": 404,
            "message": "User not found"
        }, 404)
    for u in users:
        if u['id'] == id:
            user = u
            break
    if user == None:
        return JSONResponse({
            "status": 404,
            "message": "User not found"
        }, 404)
    return JSONResponse(user, 200)

@router.get('/by_email/{email}', description="Get the info from a single user using the email")
def get_by_id(email: str = Path()):
    if not regex.match(r'^[a-z0-9!&\-#.~]+@[a-z0-9]+\.(([a-z0-9]+\.)+)?[a-z0-9]+$',email):
        return JSONResponse({
            "status": 400,
            "message": f"'{email}' is not a valid email"
        }, 404)
    user: User | None = None
    if len(users) == 0:
        return JSONResponse({
            "status": 404,
            "message": "User not found"
        }, 404)
    for u in users:
        if u['email'] == email:
            user = u
            break
    if user == None:
        return JSONResponse({
            "status": 404,
            "message": "User not found"
        }, 404)
    return JSONResponse(user, 200)

@router.put('/{id}', description="Update a user")
def update(id: str = Path(), payload: User = Body()):
    user: User | None = None
    if len(users) == 0:
        return JSONResponse({
            "status": 404,
            "message": "User does not exist"
        }, 404)
    for u in users:
        if u['id'] == id:
            payload = payload.model_dump()
            u["email"] = payload["email"]
            u["name"] = payload["name"]
            u["lastname"] = payload["lastname"]
            u["status"] = payload["status"]
            user = u
            break
    if user == None:
        return JSONResponse({
            "status": 404,
            "message": "User does not exist"
        }, 404)
    return JSONResponse({
        "status": 200,
        "message": "User updated",
        "user": user
    }, 200)

@router.delete('/{id}', description="Remove an existent user")
def delete(id: str = Path()):
    for u in users:
        if u["id"] == id:
            users.remove(u)
            return JSONResponse({
                "status": 200,
                "message": "User deleted",
                "user": u
            }, 200)
    return JSONResponse({
        "status": 404,
        "message": "User does not exist",
    }, 404)