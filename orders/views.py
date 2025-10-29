from rest_framework import viewsets, permissions, mixins
from .models import Order
from .serializers import OrderWriteSerializer, OrderReadSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).prefetch_related("items__toppings", "items__flavour")

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return OrderWriteSerializer
        return OrderReadSerializer

    def perform_create(self, serializer):
        serializer.save()
