from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..middlewares.has_access import has_access
from ..config.database import SessionLocal
from ..models.categories import Category
from ..models.expenses import Expense
from ..schemas.Expense import ExpenseSchema

router = APIRouter(prefix="/expenses")



@router.post('', dependencies=[Depends(has_access)], description="Create a new expense")
def create(expense: ExpenseSchema = Body(), data = Depends(has_access)):
    db = SessionLocal()
    category = db.query(Category).filter(Category.id == expense.category).first()
    if not category:
        return JSONResponse({
            "status": 400,
            "input": expense.category,
            "message": f"Category not found"
        }, 400)
    if category.user_id != data['payload']['id']:
        raise HTTPException(status_code=403, detail="Forbidden")
    expense = expense.model_dump()
    del expense['category']
    if category.type != "expense":
        return JSONResponse({
            "status": 400,
            "message": f"Category type is not correct"
        }, 400)

    new_expense = Expense(**expense)
    category.expenses.append(new_expense)
    db.commit()
    db.refresh(new_expense)
    return JSONResponse({
        "status": 201,
        "message": "Expense created",
        "expense": jsonable_encoder(new_expense)
    }, 201)

@router.get('', description="List all expenses")
def get_all(ge: float | None = Query(None), le: float | None = Query(None), category: int | None = Query(None)):
    db = SessionLocal()
    expense_filter = db.query(Expense)
    if ge is not None:
        if not isinstance(ge, float):
            return JSONResponse({
                "status": 400,
                "input": ge,
                "message": f"Value is not valid"
            }, 400)
        expense_filter = expense_filter.filter(Expense.amount >= ge)
    if le is not None:
        if not isinstance(le, float):
            return JSONResponse({
                "status": 400,
                "input": le,
                "message": f"Value is not valid"
            }, 400)
        expense_filter = expense_filter.filter(Expense.amount <= le)
    if category is not None:
        if not isinstance(category, int):
            return JSONResponse({
                "status": 400,
                "input": category,
                "message": f"Value is not valid"
            }, 400)
        expense_filter = expense_filter.filter(Expense.category_id == category)
    return JSONResponse(jsonable_encoder(expense_filter.all()), 200)


@router.get('/{id}', description="Get the info from a single expense using the id")
def get_by_id(id: str = Path()):
    db = SessionLocal()
    expense = db.query(Expense).filter(Expense.id == id).first()
    if not expense:
        return JSONResponse({
            "status": 404,
            "message": "Expense not found"
        }, 404)
    return JSONResponse(jsonable_encoder(expense), 200)

@router.delete('/{id}', dependencies=[Depends(has_access)], description="Remove an existent expense")
def delete(id: str = Path(), data = Depends(has_access)):
    db = SessionLocal()
    expense = db.query(Expense).filter(Expense.id == id).first()
    if not expense:
        return JSONResponse({
            "status": 404,
            "message": "Expense not found"
        }, 404)
    category = db.query(Category).filter(Category.id == expense.category_id).first()
    if category.user_id != data['payload']['id']:
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(expense)
    db.commit()

    return JSONResponse({
        "status": 200,
        "message": "Expense deleted",
        "expense": jsonable_encoder(expense)
    }, 200)