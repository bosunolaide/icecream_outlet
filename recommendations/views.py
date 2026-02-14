import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .serializers import (
    FlavourRecommendationRequestSerializer,
    FlavourRecommendationResponseSerializer,
)
from .services import recommend_flavours_for_customer

logger = logging.getLogger(__name__)


class FlavourRecommendationsAPIView(APIView):
    """
    GET  /api/recommendations/flavours/?customer_id=1&k=5
    POST /api/recommendations/flavours/ {"customer_id":1,"k":5}
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        parameters=[
            OpenApiParameter("customer_id", OpenApiTypes.INT, required=True),
            OpenApiParameter("k", OpenApiTypes.INT, required=False),
        ],
        responses=FlavourRecommendationResponseSerializer,
        description="Personalized flavour recommendations using cosine similarity over purchase history.",
    )
    def get(self, request):
        try:
            # Validate query params using the same serializer as POST
            data = {
                "customer_id": request.query_params.get("customer_id"),
                "k": request.query_params.get("k", 5),
            }
            serializer = FlavourRecommendationRequestSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            customer_id = serializer.validated_data["customer_id"]
            k = serializer.validated_data.get("k", 5)

            recs = recommend_flavours_for_customer(customer_id=customer_id, k=k)
            return Response(
                {
                    "customer_id": customer_id,
                    "k": k,
                    "method": "cosine_similarity_user_history",
                    "recommendations": recs,
                },
                status=status.HTTP_200_OK,
            )
        except Exception:
            logger.exception("Recommendation GET failed")
            return Response(
                {"detail": "Internal error generating recommendations. Check server logs."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        request=FlavourRecommendationRequestSerializer,
        responses=FlavourRecommendationResponseSerializer,
        description="Personalized flavour recommendations (POST).",
    )
    def post(self, request):
        try:
            serializer = FlavourRecommendationRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            customer_id = serializer.validated_data["customer_id"]
            k = serializer.validated_data.get("k", 5)

            recs = recommend_flavours_for_customer(customer_id=customer_id, k=k)
            return Response(
                {
                    "customer_id": customer_id,
                    "k": k,
                    "method": "cosine_similarity_user_history",
                    "recommendations": recs,
                },
                status=status.HTTP_200_OK,
            )
        except Exception:
            logger.exception("Recommendation POST failed")
            return Response(
                {"detail": "Internal error generating recommendations. Check server logs."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
