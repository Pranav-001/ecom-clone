"""
This file contains api resources for users model.
"""

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView


class UserRegistration(APIView):

    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        email = serializers.EmailField()
        password = serializers.CharField()
        confirm_password = serializers.CharField()

        def validate(self, attrs):
            if bool(attrs["password"]) ^ bool(attrs["confirm_password"]):
                raise serializers.ValidationError(
                    "Both password and confirm_password is required."
                )

            if attrs["password"] != attrs["confirm_password"]:
                raise serializers.ValidationError(
                    "Password and confirm_password did not match."
                )

            validate_password(attrs["password"])
            return attrs

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("username", "first_name", "last_name", "email")

    def post(self, request, format=None):
        serializer = self.InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={"error": serializer.error_messages},
                status=HTTP_400_BAD_REQUEST,
            )
        validated = serializer.validated_data
        validated.pop("confirm_password")

        try:
            user = User.objects.create_user(
                username=validated["username"],
                email=validated["email"],
                password=validated["password"],
            )
        except Exception as e:  # Use proper exception later
            return Response(data={"error": str(e)}, status=HTTP_400_BAD_REQUEST)

        return Response(
            data=self.OutputSerializer(instance=user).data, status=HTTP_201_CREATED
        )
