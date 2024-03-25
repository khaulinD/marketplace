from typing import Union

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import HttpResponseForbidden
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from customers.models import Account, UserInfo, UserRating
from customs import custom_print


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    user_info = UserInfoSerializer()

    class Meta:
        model = Account
        exclude = ("password", "is_superuser",  "is_staff", "is_active")

    def get_average_rating(self, obj) -> Union[float, int]:
        ratings = UserRating.objects.filter(userID=obj)
        if ratings.count() == 0:
            return 0  # Return 0 if no ratings
        return round(ratings.aggregate(models.Avg('rating'))['rating__avg'], 2)


class UserRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = ['id', 'creator', 'userID', 'rating', 'created_at']
        read_only_fields = ('creator', 'created_at')  # Assuming the creator and created_at fields should not be directly set by the user

    def create(self, validated_data):
        # Custom logic for creating a UserRating could be placed here
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Custom logic for updating a UserRating could be placed here
        return super().update(instance, validated_data)
    # def create(self, validated_data):
    #     # Попытка найти существующий рейтинг для данного creator и userID
    #     user_rating, created = UserRating.objects.update_or_create(
    #         creator=validated_data.get('creator', None),
    #         userID=validated_data.get('userID', None),
    #         defaults={'rating': validated_data.get('rating')}
    #     )
    #     return user_rating




class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("username", "password", "first_name", "last_name", "email", "is_active")

        def is_valid(self, *, raise_exception=False):
            valid = super().is_valid(raise_exception=raise_exception)

            if valid:
                if Account.objects.filter(username=self.validated_data["username"]).exists():
                    self._errors["username"] = ["username already exists"]
                    raise PermissionDenied("username already exists")
                if Account.objects.filter(email=self.validated_data["email"]).exists():
                    self._errors["email"] = ["email already exists"]
                    raise PermissionDenied("email already exists")
            return valid

        def create(self, validated_data):
            user = Account.objects.create_user(**validated_data)
            return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["is_active"] = self.user.is_active
        data["user_id"] = self.user.id
        return data


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

class JWTCookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get(
            settings.SIMPLE_JWT["REFRESH_TOKEN_NAME"]
        )
        # print("account_serializer.py: 65", self.context["request"])
        if attrs["refresh"]:
            return super().validate(attrs)
        else:
            raise InvalidToken("Token has expired")


