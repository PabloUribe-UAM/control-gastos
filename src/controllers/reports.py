from copy import copy
from fastapi import APIRouter, Body, Path, Query
from fastapi.responses import JSONResponse
from ..localstorage.users import users
from ..localstorage.categories import categories
from ..localstorage.incomes import incomes
from ..localstorage.expenses import expenses

router = APIRouter(prefix="/users/{id}/reports")

@router.get('/basic', description="Get basic report for the user")
def get_basic_report(id: str = Path()):
    user = None
    for u in users:
        if u['id'] == id:
            user = u
            break
    if user is None:
        return JSONResponse({
            "status": 404,
            "message": "User not found"
        }, 404)
    user_categories = copy(categories)
    user_income_categories = [elem for elem in user_categories if elem['user'] == id]
    user_income_categories = [elem for elem in user_income_categories if elem['type'] == 'income']
    user_expense_categories = [elem for elem in user_categories if elem['user'] == id]
    user_expense_categories = [elem for elem in user_expense_categories if elem['type'] == 'expense']
    user_incomes = []
    user_expenses = []
    total_incomes = 0.0
    total_expenses = 0.0
    for e in user_income_categories:
        user_incomes_temp = [i for i in incomes if e["id"] == i['category']]
        for l in user_incomes_temp:
            user_incomes.append(l)
    for e in user_expense_categories:
        user_expenses_temp = [i for i in expenses if e["id"] == i['category']]
        for l in user_expenses_temp:
            user_expenses.append(l)
    for i in user_incomes:
        total_incomes += i['amount']
    for i in user_expenses:
        total_expenses += i['amount']
    return JSONResponse({
        "status": 200,
        "message": "Basic report",
        "data": {
            "incomes": {
                "amount": len(user_incomes),
                "total": total_incomes
            },
            "expenses": {
                "amount": len(user_expenses),
                "total": total_expenses
            },
            "current_balance": total_incomes - total_expenses
        }
    }, 200)

@router.get('/extended', description="Get detailed report for the user")
def get_extended_report(id: str = Path()):
    user = None
    for u in users:
        if u['id'] == id:
            user = u
            break
    if user is None:
        return JSONResponse({
            "status": 404,
            "message": "User not found"
        }, 404)
    user_categories = copy(categories)
    user_income_categories = [elem for elem in user_categories if elem['user'] == id]
    user_income_categories = [elem for elem in user_income_categories if elem['type'] == 'income']
    user_expense_categories = [elem for elem in user_categories if elem['user'] == id]
    user_expense_categories = [elem for elem in user_expense_categories if elem['type'] == 'expense']

    user_income_categories_temp = []
    user_expense_categories_temp = []
    for e in user_income_categories:
        user_incomes_temp = [i for i in incomes if e["id"] == i['category']]
        etemp = copy(e)
        etemp['total'] = 0.0
        etemp['incomes'] = []
        for l in user_incomes_temp:
            etemp['total'] += l['amount']
            if not isinstance(l['date'], str):
                l['date'] = l['date'].isoformat()
            etemp['incomes'].append(l)
        user_income_categories_temp.append(etemp)
    user_income_categories = user_income_categories_temp
    for e in user_expense_categories:
        user_expenses_temp = [i for i in expenses if e["id"] == i['category']]
        etemp = copy(e)
        etemp['total'] = 0.0
        etemp['expenses'] = []
        for l in user_expenses_temp:
            etemp['total'] += l['amount']
            if not isinstance(l['date'], str):
                l['date'] = l['date'].isoformat()
            etemp['expenses'].append(l)
        user_expense_categories_temp.append(etemp)
    user_expense_categories = user_expense_categories_temp

    return JSONResponse({
        "status": 200,
        "message": "Detailed report",
        "data": {
            "income_categories": user_income_categories,
            "expense_categories": user_expense_categories
        }
    }, 200)