from fastapi import APIRouter, Body, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..config.database import SessionLocal
from ..models.categories import Category
from ..models.incomes import Income
from ..schemas.Income import IncomeSchema

router = APIRouter(prefix="/incomes")

@router.post('', description="Create a new income")
def create(income: IncomeSchema = Body()):
    db = SessionLocal()
    category = db.query(Category).filter(Category.id == income.category).first()
    if not category:
        return JSONResponse({
            "status": 400,
            "input": income.category,
            "message": f"Category not found"
        }, 400)
    income = income.model_dump()
    del income['category']
    if category.type != "income":
        return JSONResponse({
            "status": 400,
            "message": f"Category type is not correct"
        }, 400)

    new_income = Income(**income)
    category.incomes.append(new_income)
    db.commit()
    db.refresh(new_income)
    return JSONResponse({
        "status": 201,
        "message": "Income created",
        "income": jsonable_encoder(new_income)
    }, 201)

@router.get('', description="List all incomes")
def get_all(ge: float | None = Query(None), le: float | None = Query(None), category: int | None = Query(None)):
    db = SessionLocal()
    income_filter = db.query(Income)
    if ge is not None:
        if not isinstance(ge, float):
            return JSONResponse({
                "status": 400,
                "input": ge,
                "message": f"Value is not valid"
            }, 400)
        income_filter = income_filter.filter(Income.amount >= ge)
    if le is not None:
        if not isinstance(le, float):
            return JSONResponse({
                "status": 400,
                "input": le,
                "message": f"Value is not valid"
            }, 400)
        income_filter = income_filter.filter(Income.amount <= le)
    if category is not None:
        if not isinstance(category, int):
            return JSONResponse({
                "status": 400,
                "input": category,
                "message": f"Value is not valid"
            }, 400)
        income_filter = income_filter.filter(Income.category_id == category)
    return JSONResponse(jsonable_encoder(income_filter.all()), 200)


@router.get('/{id}', description="Get the info from a single income using the id")
def get_by_id(id: str = Path()):
    db = SessionLocal()
    income = db.query(Income).filter(Income.id == id).first()
    if not income:
        return JSONResponse({
            "status": 404,
            "message": "Income not found"
        }, 404)
    return JSONResponse(jsonable_encoder(income), 200)

@router.delete('/{id}', description="Remove an existent income")
def delete(id: str = Path()):
    db = SessionLocal()
    income = db.query(Income).filter(Income.id == id).first()
    if not income:
        return JSONResponse({
            "status": 404,
            "message": "Income not found"
        }, 404)

    db.delete(income)
    db.commit()

    return JSONResponse({
        "status": 200,
        "message": "Income deleted",
        "expense": jsonable_encoder(income)
    }, 200)