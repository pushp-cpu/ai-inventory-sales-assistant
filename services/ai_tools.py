from services.database_service import (
    get_all_products,
    get_all_sales,
    get_best_selling_products,
    get_low_stock_products,
    get_total_revenue,
)


def get_products_tool():
    return get_all_products()


def get_sales_tool():
    return get_all_sales()


def get_low_stock_tool():
    return get_low_stock_products()


def get_revenue_tool():
    return {"total_revenue": get_total_revenue()}


def get_best_selling_tool():
    return get_best_selling_products()


TOOLS = {
    "get_products": get_products_tool,
    "get_sales": get_sales_tool,
    "get_low_stock_products": get_low_stock_tool,
    "get_total_revenue": get_revenue_tool,
    "get_best_selling_products": get_best_selling_tool,
}