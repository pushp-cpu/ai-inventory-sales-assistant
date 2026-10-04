from database import get_connection


def add_product(name, category, price, stock_quantity, reorder_level):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO products
        (name, category, price, stock_quantity, reorder_level)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (
        name,
        category,
        price,
        stock_quantity,
        reorder_level
    ))

    product_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return product_id


def get_all_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            products.id,
            products.name,
            products.category,
            products.price,
            products.stock_quantity,
            products.reorder_level,
            suppliers.name
        FROM products
        LEFT JOIN suppliers
            ON products.supplier_id = suppliers.id
        ORDER BY products.id
    """)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products


def add_supplier(name, email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO suppliers
        (name, email)
        VALUES (%s, %s)
        RETURNING id
    """, (
        name,
        email
    ))

    supplier_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return supplier_id


def get_all_suppliers():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            email
        FROM suppliers
        ORDER BY id
    """)

    suppliers = cursor.fetchall()

    cursor.close()
    connection.close()

    return suppliers


def record_sale(product_id, quantity):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT price, stock_quantity
        FROM products
        WHERE id = %s
    """, (product_id,))

    product = cursor.fetchone()

    if product is None:
        cursor.close()
        connection.close()
        raise ValueError("Product not found.")

    price, stock_quantity = product

    if quantity <= 0:
        cursor.close()
        connection.close()
        raise ValueError("Quantity must be greater than 0.")

    if quantity > stock_quantity:
        cursor.close()
        connection.close()
        raise ValueError("Not enough stock available.")

    total_amount = price * quantity

    cursor.execute("""
        INSERT INTO sales
        (product_id, quantity, total_amount)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (
        product_id,
        quantity,
        total_amount
    ))

    sale_id = cursor.fetchone()[0]

    cursor.execute("""
        UPDATE products
        SET stock_quantity = stock_quantity - %s
        WHERE id = %s
    """, (
        quantity,
        product_id
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return sale_id


def get_all_sales():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            sales.id,
            products.name,
            sales.quantity,
            sales.total_amount,
            sales.sale_date
        FROM sales
        JOIN products
            ON sales.product_id = products.id
        ORDER BY sales.id
    """)

    rows = cursor.fetchall()

    sales = []

    for row in rows:
        sales.append({
            "id": row[0],
            "product_name": row[1],
            "quantity": row[2],
            "total_amount": float(row[3]),
            "sale_date": row[4].isoformat()
        })

    cursor.close()
    connection.close()


    return sales


def get_low_stock_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            category,
            stock_quantity,
            reorder_level
        FROM products
        WHERE stock_quantity <= reorder_level
        ORDER BY stock_quantity
    """)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products


def get_total_revenue():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(total_amount), 0)
        FROM sales
    """)

    total_revenue = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total_revenue


def get_best_selling_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            products.name,
            SUM(sales.quantity) AS total_quantity_sold
        FROM sales
        JOIN products
            ON sales.product_id = products.id
        GROUP BY products.id, products.name
        ORDER BY total_quantity_sold DESC
    """)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products


def assign_supplier_to_product(product_id, supplier_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM suppliers
        WHERE id = %s
    """, (supplier_id,))

    supplier = cursor.fetchone()

    if supplier is None:
        cursor.close()
        connection.close()
        raise ValueError("Supplier not found.")

    cursor.execute("""
        UPDATE products
        SET supplier_id = %s
        WHERE id = %s
    """, (
        supplier_id,
        product_id
    ))

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        raise ValueError("Product not found.")

    connection.commit()

    cursor.close()
    connection.close()