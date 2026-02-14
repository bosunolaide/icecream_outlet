from rest_framework import serializers

class FlavourRecommendationRequestSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    k = serializers.IntegerField(required=False, default=5, min_value=1, max_value=50)

class FlavourRecommendationItemSerializer(serializers.Serializer):
    flavour_id = serializers.IntegerField()
    name = serializers.CharField()
    score = serializers.FloatField()

class FlavourRecommendationResponseSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    k = serializers.IntegerField()
    method = serializers.CharField()
    recommendations = FlavourRecommendationItemSerializer(many=True)
