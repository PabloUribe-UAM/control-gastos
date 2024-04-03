from copy import deepcopy
from typing import List
from fastapi import APIRouter, Body, Path, Query
from fastapi.responses import JSONResponse
from ..localstorage.expenses import expenses
from ..localstorage.categories import categories
from ..models.Expense import Expense

router = APIRouter(prefix="/expenses")



@router.post('', description="Create a new expense")
def create(expense: Expense = Body()):
    cat = None
    for e in categories:
        if e['id'] == expense.category:
            cat = e
    if cat is None:
        return JSONResponse({
            "status": 400,
            "input": expense.category,
            "message": f"Category not found"
        }, 400)
    expenses.append(expense.model_dump())
    expense.date = expense.date.isoformat()
    return JSONResponse({
        "status": 201,
        "message": "Expense created",
        "expense": expense.model_dump()
    }, 201)

@router.get('', description="List all expenses")
def get_all(ge: float | None = Query(None), le: float | None = Query(None), category: int | None = Query(None)):
    expense_filter: List[Expense] = deepcopy(expenses)
    if ge is not None:
        if not isinstance(ge, float):
            return JSONResponse({
                "status": 400,
                "input": ge,
                "message": f"Value is not valid"
            }, 400)
        expense_filter = [elem for elem in expense_filter if elem['amount'] >= ge]
    if le is not None:
        if not isinstance(le, float):
            return JSONResponse({
                "status": 400,
                "input": le,
                "message": f"Value is not valid"
            }, 400)
        expense_filter = [elem for elem in expense_filter if elem['amount'] <= le]
    if category is not None:
        if not isinstance(category, int):
            return JSONResponse({
                "status": 400,
                "input": category,
                "message": f"Value is not valid"
            }, 400)
        expense_filter = [elem for elem in expense_filter if elem['category'] == category]
    for e in expense_filter:
        if not isinstance(e['date'], str):
            e['date'] = e['date'].isoformat()
    return JSONResponse(expense_filter, 200)


@router.get('/{id}', description="Get the info from a single expense using the id")
def get_by_id(id: str = Path()):
    expense: Expense | None = None
    if len(expenses) == 0:
        return JSONResponse({
            "status": 404,
            "message": "Expense not found"
        }, 404)
    for e in expenses:
        if e['id'] == id:
            expense = e
            break
    expense['date'] = expense['date'].isoformat()
    if expense == None:
        return JSONResponse({
            "status": 404,
            "message": "Expense not found"
        }, 404)
    return JSONResponse(expense, 200)

@router.delete('/{id}', description="Remove an existent expense")
def delete(id: str = Path()):
    for e in expenses:
        if e["id"] == id:
            expenses.remove(e)
            if not isinstance(e['date'], str):
                e["date"] = e["date"].isoformat()
            return JSONResponse({
                "status": 200,
                "message": "Expense deleted",
                "expense": e
            }, 200)
    return JSONResponse({
        "status": 404,
        "message": "Expense does not exist",
    }, 404)