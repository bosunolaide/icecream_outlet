from rest_framework import viewsets, permissions
from .models import Topping
from .serializers import ToppingSerializer

class ToppingViewSet(viewsets.ModelViewSet):
    queryset = Topping.objects.all()
    serializer_class = ToppingSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
