from django.shortcuts import render
from .models import User
from typing import Any

from django.contrib.auth.hashers import make_password
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "password",
            "role",
        ]
    
    def validate(self, attrs: dict[str, Any]):
        """Change the password for its hash to make Token-based authentication available."""

        attrs["password"] = make_password(attrs["password"])
        attrs["is_active"] = True

        return super().validate(attrs=attrs)


class UsersAPIViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]

    def create(self, request: Request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(UserSerializer(serializer.instance).data, status=201)



router = routers.DefaultRouter()
router.register(r"", UsersAPIViewSet, basename="user")