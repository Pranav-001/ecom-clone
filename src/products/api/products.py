"""
This file contains api resources for products model.
"""

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from products.models import Category, Product


class ProductAPI(APIView):
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        price = serializers.FloatField(min_value=0.01)
        stock_quantity = serializers.IntegerField(min_value=0)
        category_id = serializers.IntegerField()

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("name", "price", "stock_quantity", "category__name")

    def post(self, request, format=None):
        serializer = self.InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={"error": serializer.error_messages},
                status=HTTP_400_BAD_REQUEST,
            )
        validated = serializer.validated_data

        try:
            product = Product.objects.create(
                name=validated["name"],
                price=validated["price"],
                stock_quantity=validated["stock_quantity"],
                category_id=validated["category_id"],
            )
        except Exception as e:  # Use proper exception later
            return Response(data={"error": str(e)}, status=HTTP_400_BAD_REQUEST)

        return Response(
            data=self.OutputSerializer(instance=product).data, status=HTTP_201_CREATED
        )
