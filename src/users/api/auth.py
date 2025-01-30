"""
This file contains api resources for users authentication.
"""

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserLoginAPI(APIView):

    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

    def post(self, request, format=None):
        serializer = self.InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={"error": serializer.error_messages},
                status=HTTP_400_BAD_REQUEST,
            )
        validated = serializer.validated_data
        user = authenticate(
            username=validated["username"], password=validated["password"]
        )
        if not user:
            return Response(
                data={"error": "Username or password is incorrect."},
                status=HTTP_400_BAD_REQUEST,
            )
        token = TokenObtainPairSerializer.get_token(user=user)
        return Response(
            data={
                "access_token": str(token.access_token),
                "refresh_token": str(token),  # move to cookies
            },
            status=HTTP_200_OK,
        )
