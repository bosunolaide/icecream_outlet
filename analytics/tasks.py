
from celery import shared_task
from django.db import connections
from django.utils import timezone
@shared_task
def sync_to_analytics():
    with connections["default"].cursor() as pg, connections["analytics"].cursor() as my:
        my.execute("""
            CREATE TABLE IF NOT EXISTS analytics_order (
                id INT PRIMARY KEY,
                customer_id INT NOT NULL,
                total DECIMAL(10,2) NOT NULL,
                created_at DATETIME NOT NULL
            )
        """)
        pg.execute("SELECT id, customer_id, total, created_at FROM orders_order")
        rows = pg.fetchall()
        my.execute("DELETE FROM analytics_order")
        if rows:
            my.executemany(
                "INSERT INTO analytics_order (id, customer_id, total, created_at) VALUES (%s, %s, %s, %s)",
                rows,
            )
    return {"rows_synced": len(rows), "timestamp": timezone.now().isoformat()}
@shared_task
def train_sales_forecast():
    import pandas as pd
    with connections["analytics"].cursor() as my:
        my.execute("SELECT DATE(created_at) as d, SUM(total) as revenue FROM analytics_order GROUP BY DATE(created_at)")
        data = my.fetchall()
    df = pd.DataFrame(data, columns=["date", "revenue"]).sort_values("date")
    return {"n_days": int(df.shape[0])}
