from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from .serializers import (
    FlavourRecommendationRequestSerializer,
    FlavourRecommendationResponseSerializer,
)
from .services import recommend_flavours_for_customer

class FlavourRecommendationsAPIView(APIView):

    @extend_schema(
        request=FlavourRecommendationRequestSerializer,
        responses=FlavourRecommendationResponseSerializer,
        description="Personalized flavour recommendations using cosine similarity over purchase history."
    )
    def post(self, request):
        serializer = FlavourRecommendationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = serializer.validated_data["customer_id"]
        k = serializer.validated_data.get("k", 5)

        recs = recommend_flavours_for_customer(customer_id=customer_id, k=k)
        payload = {
            "customer_id": customer_id,
            "k": k,
            "method": "cosine_similarity_user_history",
            "recommendations": recs,
        }
        return Response(payload, status=status.HTTP_200_OK)

    @extend_schema(
        responses=FlavourRecommendationResponseSerializer,
        description="Personalized flavour recommendations (query params: customer_id, k)."
    )
    def get(self, request):
        customer_id = request.query_params.get("customer_id")
        k = request.query_params.get("k", "5")

        try:
            customer_id = int(customer_id) if customer_id is not None else None
            k = int(k)
        except ValueError:
            return Response({"detail": "customer_id and k must be integers"}, status=status.HTTP_400_BAD_REQUEST)

        if customer_id is None:
            return Response({"detail": "customer_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        recs = recommend_flavours_for_customer(customer_id=customer_id, k=k)
        payload = {
            "customer_id": customer_id,
            "k": k,
            "method": "cosine_similarity_user_history",
            "recommendations": recs,
        }
        return Response(payload, status=status.HTTP_200_OK)
