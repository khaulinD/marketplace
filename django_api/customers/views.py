import logging

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, generics
from django_ratelimit.decorators import ratelimit
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from verify_email.email_handler import send_verification_email

from .email_verification.emails import verification_email
from .email_verification.utils import generate_token
from .filters.account_filter import AccountFilter
from .models import Account, UserRating
from .serializers.account_serializer import AccountSerializer, RegisterSerializer, \
    LogoutSerializer, CustomTokenObtainPairSerializer, JWTCookieTokenRefreshSerializer, UserRatingSerializer

logger = logging.getLogger("django_api")


class AccountViewSet(viewsets.ViewSet):
    """ account class return list of user or one user """
    # permission_classes = [IsAuthenticated]
    queryset = Account.objects.select_related("user_info").all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AccountFilter

    @method_decorator(ratelimit(key='ip', rate='10/m', method='GET', block=True))
    def list(self, request):
        queryset = self.filterset_class(request.GET, self.queryset).qs
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class RegisterViewSet(viewsets.ViewSet):
    """ registration class """

    serializer_class = RegisterSerializer

    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            # username = request.data.get('username')
            forbidden_usernames = ["admin", "root", "superuser"]
            print(serializer.validated_data)
            if username in forbidden_usernames:
                return Response({"error": "Username not allowed"}, status=status.HTTP_409_CONFLICT)
            serializer.save()
            try:
                 verification_email(username, request)
            except Exception as e:
                logger.error(str(e))
                return HttpResponse("Can`t send verification email", status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        errors = serializer.errors
        if "username" in errors and "non_field_errors" not in errors:
            return Response({"error": "Username already exists"}, status=status.HTTP_409_CONFLICT)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(viewsets.ViewSet):
    serializer_class = LogoutSerializer


    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            refresh_token = serializer.validated_data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            # print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class JWTSetCookieMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                settings.SIMPLE_JWT["REFRESH_TOKEN_NAME"],
                response.data["refresh"],
                max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                httponly=True,
                samesite=settings.SIMPLE_JWT["JWT_COOKIE_SAMESITE"],
            )
        if response.data.get("access"):
            response.set_cookie(

                settings.SIMPLE_JWT["ACCESS_TOKEN_NAME"],
                response.data["access"],
                max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                httponly=True,
                samesite=settings.SIMPLE_JWT["JWT_COOKIE_SAMESITE"],
            )
            del response.data["access"]

        return super().finalize_response(request, response, *args, **kwargs)


class JWTCookieTokenObtainPairView(JWTSetCookieMixin, TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class JWTCookieTokenRefreshView(JWTSetCookieMixin, TokenRefreshView):
    serializer_class = JWTCookieTokenRefreshSerializer



def activate_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist) as e:
        logger.warning(str(e))
        user = None

    if user and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("User activated successfully")

    return HttpResponse("Activation failed", status=status.HTTP_400_BAD_REQUEST)


class UserRatingView(viewsets.ViewSet):
    serializer_class = UserRatingSerializer
    # permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        # Automatically set the creator to the current user during creation
        serializer.save(creator=self.request.user)

    def create(self, request, *args, **kwargs):
        rating_exists = UserRating.objects.filter(creator=request.user, userID=request.data["userID"]).first()
        if not rating_exists:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if rating_exists.rating != request.data["rating"]:
                serializer = self.serializer_class(instance=rating_exists, data=request.data)
                if serializer.is_valid():
                    self.perform_create(serializer)
                    # serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return HttpResponse("You already set this rating", status=status.HTTP_409_CONFLICT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
