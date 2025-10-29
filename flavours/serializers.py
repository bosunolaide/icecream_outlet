from rest_framework import serializers
from .models import Flavour

class FlavourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavour
        fields = "__all__"
