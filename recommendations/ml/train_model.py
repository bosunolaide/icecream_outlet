import pandas as pd
from sklearn.neighbors import NearestNeighbors
import joblib
from orders.models import OrderItem

def train_flavour_recommender():
    items = OrderItem.objects.select_related("order", "flavour")
    data = [
        {"user_id": i.order.customer_id, "flavour_id": i.flavour_id, "quantity": i.quantity}
        for i in items
    ]
    df = pd.DataFrame(data)

    if df.empty:
        print("⚠️ No order data available for training.")
        return

    pivot = df.pivot_table(index="user_id", columns="flavour_id", values="quantity", fill_value=0)

    model = NearestNeighbors(metric="cosine", algorithm="brute")
    model.fit(pivot.values)

    joblib.dump({
        "model": model,
        "flavours": list(pivot.columns),
        "users": list(pivot.index)
    }, "ml_models/flavour_recommender.pkl")

    print("✅ Flavour recommender trained and saved.")
