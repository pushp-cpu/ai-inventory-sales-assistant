from fastapi import APIRouter
from pydantic import BaseModel
from services.ai_service import ask_gemini


from services.database_service import (
    get_all_products,
    get_all_sales,
    get_all_suppliers,
    get_best_selling_products,
    get_low_stock_products,
    get_total_revenue,
)

router = APIRouter()


@router.get("/products")
def products():
    return get_all_products()


@router.get("/suppliers")
def suppliers():
    return get_all_suppliers()


@router.get("/sales")
def sales():
    return get_all_sales()


@router.get("/reports/revenue")
def revenue():
    return {
        "total_revenue": get_total_revenue()
    }


@router.get("/reports/low-stock")
def low_stock():
    return {
        "products": get_low_stock_products()
    }


@router.get("/reports/best-selling")
def best_selling():
    return {
        "products": get_best_selling_products()
    }

class AskRequest(BaseModel):
    question: str


@router.post("/ask")
def ask(request: AskRequest):
    answer = ask_gemini(request.question)

    return {
        "question": request.question,
        "answer": answer
    }