from typing import List
from fastapi import APIRouter, Body, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..models.categories import Category

from ..config.database import SessionLocal
from ..schemas.Category import CategorySchema
import re as regex

router = APIRouter(prefix="/categories")


@router.post('', description="Create a new category")
def create(category: CategorySchema = Body()):
    db = SessionLocal()
    new_category = Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    return JSONResponse({
        "status": 201,
        "message": "Category created",
        "category": category.model_dump()
    }, 201)

@router.get('', description="List all categories")
def get_all(type: str | None = Query(None)):
    db = SessionLocal()
    category_filter = db.query(Category)
    if type is not None:
        if not regex.match(r'^((income)|(expense))$', type):
            return JSONResponse({
                "status": 400,
                "message": f"Not recognized value '{type}'"
            }, 400)
        category_filter = category_filter.filter(Category.type == type)
        return JSONResponse(jsonable_encoder(category_filter.all()), 200)
    return JSONResponse(jsonable_encoder(category_filter.all()), 200)

@router.get('/{id}', description="Get the info from a single category using the id")
def get_by_id(id: int = Path()):
    db = SessionLocal()
    category = db.query(Category).filter(Category.id == id).first()
    if category is None:
        return JSONResponse({
            "status": 404,
            "message": "Category not found"
        }, 404)
    return JSONResponse(jsonable_encoder(category), 200)

@router.put('/{id}', description="Update a category")
def update(id: int = Path(), payload: CategorySchema = Body()):
    db = SessionLocal()
    category = db.query(Category).filter(Category.id == id).first()
    if category is None:
        return JSONResponse({
            "status": 404,
            "message": "Category does not exist"
        }, 404)
    category.type = payload.type
    category.name = payload.name
    category.description = payload.description
    db.commit()
    db.refresh(category)

    return JSONResponse({
        "status": 200,
        "message": "User updated",
        "category": jsonable_encoder(category)
    }, 200)

@router.delete('/{id}', description="Remove an existent category")
def delete(id: int = Path()):
    db = SessionLocal()
    category = db.query(Category).filter(Category.id == id).first()
    if category is None:
        return JSONResponse({
            "status": 404,
            "message": "Category does not exist",
        }, 404)
    db.delete(category)
    db.commit()
    return JSONResponse({
        "status": 200,
        "message": "Category deleted",
        "category": jsonable_encoder(category)
    }, 200)