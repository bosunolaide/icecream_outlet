
from django.db import models
class OrderAnalytics(models.Model):
    id = models.IntegerField(primary_key=True)
    customer_id = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    class Meta:
        app_label = "analytics"
        db_table = "analytics_order"
