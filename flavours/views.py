from rest_framework import viewsets, permissions
from .models import Flavour
from .serializers import FlavourSerializer

class FlavourViewSet(viewsets.ModelViewSet):
    queryset = Flavour.objects.all()
    serializer_class = FlavourSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
