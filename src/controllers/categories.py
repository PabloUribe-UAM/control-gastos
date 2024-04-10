from typing import List
from fastapi import APIRouter, Body, Path, Query
from fastapi.responses import JSONResponse
from ..localstorage.categories import categories
from ..schemas.Category import Category
import re as regex
from ..localstorage.id_control import idCategory

def id_increment():
    global idCategory
    idCategory = idCategory + 1
    return idCategory

router = APIRouter(prefix="/categories")


@router.post('', description="Create a new category")
def create(category: Category = Body()):
    category.id = id_increment()
    categories.append(category.model_dump())
    return JSONResponse({
        "status": 201,
        "message": "Category created",
        "category": category.model_dump()
    }, 201)

@router.get('', description="List all categories")
def get_all(type: str | None = Query(None)):
    category_filter: List[Category] = []
    if type is not None:
        if not regex.match(r'^((income)|(expense))$', type):
            return JSONResponse({
                "status": 400,
                "message": f"Not recognized value '{type}'"
            }, 400)
        for elem in categories:
            if elem['type'] == type:
                category_filter.append(elem)
        return JSONResponse(category_filter, 200)
    return JSONResponse(categories, 200)

@router.get('/{id}', description="Get the info from a single category using the id")
def get_by_id(id: int = Path()):
    category: Category | None = None
    if len(categories) == 0:
        return JSONResponse({
            "status": 404,
            "message": "Category not found"
        }, 404)
    for c in categories:
        if c['id'] == id:
            category = c
            break
    if category == None:
        return JSONResponse({
            "status": 404,
            "message": "Category not found"
        }, 404)
    return JSONResponse(category, 200)

@router.put('/{id}', description="Update a category")
def update(id: int = Path(), payload: Category = Body()):
    category: Category | None = None
    if len(categories) == 0:
        return JSONResponse({
            "status": 404,
            "message": "Category does not exist"
        }, 404)
    for c in categories:
        if c['id'] == id:
            payload = payload.model_dump()
            c["type"] = payload["type"]
            c["name"] = payload["name"]
            c["description"] = payload["description"]
            category = c
            break
    if category == None:
        return JSONResponse({
            "status": 404,
            "message": "Category does not exist"
        }, 404)
    return JSONResponse({
        "status": 200,
        "message": "User updated",
        "category": category
    }, 200)

@router.delete('/{id}', description="Remove an existent category")
def delete(id: int = Path()):
    for c in categories:
        if c["id"] == id:
            categories.remove(c)
            return JSONResponse({
                "status": 200,
                "message": "Category deleted",
                "category": c
            }, 200)
    return JSONResponse({
        "status": 404,
        "message": "Category does not exist",
    }, 404)