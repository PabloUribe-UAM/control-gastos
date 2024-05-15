from copy import copy
from fastapi import APIRouter, Body, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.config.database import SessionLocal
from src.models.categories import Category

router = APIRouter(prefix="/users/{id}/reports")

@router.get('/basic', description="Get basic report for the user")
def get_basic_report(id: str = Path()):
    db = SessionLocal()
    incomes = db.query(Category).filter(Category.user_id == id).filter(Category.type == "income")
    expenses = db.query(Category).filter(Category.user_id == id).filter(Category.type == "expense")
    income_amount = 0.0
    expense_amount = 0.0
    total_incomes = 0
    total_expenses = 0
    for i in incomes:
        income_amount += len(i.incomes)
        for j in i.incomes:
            total_incomes += j.amount
    for e in expenses:
        expense_amount += len(e.expenses)
        for j in e.expenses:
            total_expenses += j.amount
    return JSONResponse({
        "status": 200,
        "message": "Basic report",
        "data": {
            "incomes": {
                "amount": income_amount,
                "total": total_incomes
            },
            "expenses": {
                "amount": expense_amount,
                "total": total_expenses
            },
            "current_balance": total_incomes - total_expenses
        }
    }, 200)

@router.get('/detailed', description="Get detailed report for the user")
def get_extended_report(id: str = Path()):
    user_income_categories = []
    user_expense_categories = []
    db = SessionLocal()
    incomes = db.query(Category).filter(Category.user_id == id).filter(Category.type == "income")
    expenses = db.query(Category).filter(Category.user_id == id).filter(Category.type == "expense")

    for i in incomes:
        cat = {
            "name": i.name,
            "total": 0.0,
            "incomes": []
        }
        for j in i.incomes:
            cat["total"] += j.amount
            cat["incomes"].append({
                "description": j.description,
                "amount": j.amount,
                "date": jsonable_encoder(j.date)
            })
        user_income_categories.append(cat)
    for i in expenses:
        cat = {
            "name": i.name,
            "total": 0.0,
            "expenses": []
        }
        for j in i.expenses:
            cat["total"] += j.amount
            cat["expenses"].append({
                "description": j.description,
                "amount": j.amount,
                "date": jsonable_encoder(j.date)
            })
        user_expense_categories.append(cat)
    return JSONResponse({
        "status": 200,
        "message": "Detailed report",
        "data": {
            "income_categories": user_income_categories,
            "expense_categories": user_expense_categories
        }
    }, 200)