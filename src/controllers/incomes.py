from copy import deepcopy
from typing import List
from fastapi import APIRouter, Body, Path, Query
from fastapi.responses import JSONResponse
from ..localstorage.incomes import incomes
from ..localstorage.categories import categories
from ..models.Income import Income

router = APIRouter(prefix="/incomes")


@router.post('', description="Create a new income")
def create(income: Income = Body()):
    cat = None
    for e in categories:
        if e['id'] == income.category:
            cat = e
    if cat is None:
        return JSONResponse({
            "status": 400,
            "input": income.category,
            "message": f"Category not found"
        }, 400)
    incomes.append(income.model_dump())
    income.date = income.date.isoformat()
    return JSONResponse({
        "status": 201,
        "message": "Income created",
        "income": income.model_dump()
    }, 201)

@router.get('', description="List all incomes")
def get_all(ge: float | None = Query(None), le: float | None = Query(None), category: int | None = Query(None)):
    income_filter: List[Income] = deepcopy(incomes)
    if ge is not None:
        if not isinstance(ge, float):
            return JSONResponse({
                "status": 400,
                "input": ge,
                "message": f"Value is not valid"
            }, 400)
        income_filter = [elem for elem in income_filter if elem['amount'] >= ge]
    if le is not None:
        if not isinstance(le, float):
            return JSONResponse({
                "status": 400,
                "input": le,
                "message": f"Value is not valid"
            }, 400)
        income_filter = [elem for elem in income_filter if elem['amount'] <= le]
    if category is not None:
        if not isinstance(category, int):
            return JSONResponse({
                "status": 400,
                "input": category,
                "message": f"Value is not valid"
            }, 400)
        income_filter = [elem for elem in income_filter if elem['category'] == category]
    for e in income_filter:
        if not isinstance(e['date'], str):
            e['date'] = e['date'].isoformat()
    return JSONResponse(income_filter, 200)


@router.get('/{id}', description="Get the info from a single income using the id")
def get_by_id(id: str = Path()):
    income: Income | None = None
    if len(incomes) == 0:
        return JSONResponse({
            "status": 404,
            "message": "Income not found"
        }, 404)
    for i in incomes:
        if i['id'] == id:
            income = i
            break
    income['date'] = income['date'].isoformat()
    if income == None:
        return JSONResponse({
            "status": 404,
            "message": "Income not found"
        }, 404)
    return JSONResponse(income, 200)

@router.delete('/{id}', description="Remove an existent income")
def delete(id: str = Path()):
    for i in incomes:
        if i["id"] == id:
            incomes.remove(i)
            if not isinstance(i['date'], str):
                i["date"] = i["date"].isoformat()
            return JSONResponse({
                "status": 200,
                "message": "Income deleted",
                "income": i
            }, 200)
    return JSONResponse({
        "status": 404,
        "message": "Income does not exist",
    }, 404)