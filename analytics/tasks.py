from celery import shared_task
from django.db import connections
from django.utils import timezone

@shared_task
def sync_to_analytics():
    """
    Hourly sync from Postgres (default) -> MySQL (analytics).

    IMPORTANT:
    - Order.total is a Python property, not a DB column.
    - We compute totals in SQL using OrderItem + Flavour + Toppings tables.

    Strategy:
    - Truncate + insert for clarity (safe for small/medium datasets).
    - For production scale: do incremental upserts using updated_at and/or CDC.
    """
    # SQL is written to be compatible with Postgres (source) and MySQL (target table schema).
    order_totals_sql = """
        SELECT
            o.id AS id,
            o.customer_id AS customer_id,
            COALESCE(fl.total_flavour, 0) + COALESCE(tp.total_toppings, 0) AS total,
            o.created_at AS created_at
        FROM orders_order o
        LEFT JOIN (
            SELECT
                oi.order_id AS order_id,
                SUM(f.price * oi.quantity) AS total_flavour
            FROM orders_orderitem oi
            JOIN flavours_flavour f ON f.id = oi.flavour_id
            GROUP BY oi.order_id
        ) fl ON fl.order_id = o.id
        LEFT JOIN (
            SELECT
                oi.order_id AS order_id,
                SUM(t.price * oi.quantity) AS total_toppings
            FROM orders_orderitem oi
            JOIN orders_orderitem_toppings oit ON oit.orderitem_id = oi.id
            JOIN toppings_topping t ON t.id = oit.topping_id
            GROUP BY oi.order_id
        ) tp ON tp.order_id = o.id
        ;
    """

    with connections["default"].cursor() as pg, connections["analytics"].cursor() as my:
        # Ensure destination table exists (MySQL)
        my.execute("""
            CREATE TABLE IF NOT EXISTS analytics_order (
                id INT PRIMARY KEY,
                customer_id INT NOT NULL,
                total DECIMAL(10,2) NOT NULL,
                created_at DATETIME NOT NULL
            )
        """)

        pg.execute(order_totals_sql)
        rows = pg.fetchall()

        my.execute("DELETE FROM analytics_order")
        if rows:
            my.executemany(
                "INSERT INTO analytics_order (id, customer_id, total, created_at) VALUES (%s, %s, %s, %s)",
                rows,
            )

    return {"rows_synced": len(rows), "timestamp": timezone.now().isoformat()}
