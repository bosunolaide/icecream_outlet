from django.db import models
from django.conf import settings

class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.CharField(max_length=255, blank=True)

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        CANCELLED = "CANCELLED", "Cancelled"
        FULFILLED = "FULFILLED", "Fulfilled"

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"Order #{self.pk} by {self.customer}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    flavour = models.ForeignKey("flavours.Flavour", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    toppings = models.ManyToManyField("toppings.Topping", blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.flavour.name}"

    @property
    def subtotal(self):
        flavour_price = self.flavour.price * self.quantity
        toppings_total = sum(t.price for t in self.toppings.all()) * self.quantity
        return flavour_price + toppings_total
