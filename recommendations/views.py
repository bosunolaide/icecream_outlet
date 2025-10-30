from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from flavours.serializers import FlavourSerializer
from .ml.recommender import FlavourRecommender

class RecommendFlavoursView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recommender = FlavourRecommender()
        recommendations = recommender.recommend_for_user(request.user.id)
        serializer = FlavourSerializer(recommendations, many=True)
        return Response(serializer.data)
