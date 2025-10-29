from rest_framework import serializers
from .models import Order, OrderItem
from flavours.models import Flavour
from toppings.models import Topping

class OrderItemWriteSerializer(serializers.ModelSerializer):
    toppings = serializers.PrimaryKeyRelatedField(queryset=Topping.objects.all(), many=True, required=False)

    class Meta:
        model = OrderItem
        fields = ("flavour", "quantity", "toppings")

class OrderItemReadSerializer(serializers.ModelSerializer):
    flavour = serializers.StringRelatedField()
    toppings = serializers.StringRelatedField(many=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "flavour", "quantity", "toppings", "subtotal")

class OrderWriteSerializer(serializers.ModelSerializer):
    items = OrderItemWriteSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "notes", "items")

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        user = self.context["request"].user
        order = Order.objects.create(customer=user, **validated_data)
        for item in items_data:
            toppings = item.pop("toppings", [])
            order_item = OrderItem.objects.create(order=order, **item)
            if toppings:
                order_item.toppings.set(toppings)
        return order

class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "status", "notes", "created_at", "updated_at", "items", "total")
