from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers

from rest_framework_simplejwt.views import TokenVerifyView

from customers import views

router = routers.DefaultRouter()
router.register(r'accounts', views.AccountViewSet, basename='account')
router.register(r'register', views.RegisterViewSet, basename='account')
router.register(r'logout', views.LogoutView, basename='account')
router.register(r'user-ratings', views.UserRatingView, basename='account')

# user_router = routers.NestedDefaultRouter(router, "accounts", lookup="account")
# user_router.register(r'ratings', views.UserRatingsView, basename='rating')


urlpatterns_customers = [
    path('api/token/', views.JWTCookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', views.JWTCookieTokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("api/", include(router.urls)),
    # path("api/", include(user_router.urls)),
    #  path("api/user-ratings", views.UserRatingCreateUpdateAPIView.as_view()),

    path("verification/<uidb64>/<token>/", views.activate_user, name='activate_user'),
]