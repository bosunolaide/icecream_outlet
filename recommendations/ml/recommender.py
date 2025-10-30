import joblib
from flavours.models import Flavour
from orders.models import OrderItem

class FlavourRecommender:
    def __init__(self):
        data = joblib.load("ml_models/flavour_recommender.pkl")
        self.model = data["model"]
        self.flavour_ids = data["flavours"]
        self.user_ids = data["users"]

    def recommend_for_user(self, user_id, n=3):
        if user_id not in self.user_ids:
            return Flavour.objects.order_by("price")[:n]

        user_index = self.user_ids.index(user_id)
        distances, indices = self.model.kneighbors(
            [self.model._fit_X[user_index]], n_neighbors=n+1
        )
        similar_users = [self.user_ids[i] for i in indices.flatten() if i != user_id]

        rec_flavours = (
            OrderItem.objects.filter(order__customer_id__in=similar_users)
            .values_list("flavour_id", flat=True)
            .distinct()[:n]
        )
        return Flavour.objects.filter(id__in=rec_flavours)
