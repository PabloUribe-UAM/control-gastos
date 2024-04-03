from fastapi import FastAPI
from .controllers.users import router as user_routes
from .controllers.reports import router as report_routes
from .controllers.categories import router as category_routes
from .controllers.incomes import router as income_routes
from .controllers.expenses import router as expense_routes

metadata = [
    {
        "name": "web",
        "description": "Web endpoints"
    },
    {
        "name": "users",
        "description": "User handle endpoints"
    },
    {
        "name": "reports",
        "description": "Report handle endpoints"
    },
    {
        "name": "categories",
        "description": "Category handle endpoints"
    },
    {
        "name": "incomes",
        "description": "Income handle endpoints"
    },
    {
        "name": "expenses",
        "description": "Expense handle endpoints"
    }
]

app = FastAPI(openapi_tags=metadata, root_path="/api/v1")


app.include_router(user_routes, tags=["users"])
app.include_router(report_routes, tags=["reports"])
app.include_router(category_routes, tags=["categories"])
app.include_router(income_routes, tags=["incomes"])
app.include_router(expense_routes, tags=["expenses"])