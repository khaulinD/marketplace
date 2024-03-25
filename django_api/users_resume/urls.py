from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers

from rest_framework_simplejwt.views import TokenVerifyView

from users_resume import views

router = routers.DefaultRouter()
router.register(r'resume', views.ResumeViewSet, basename='resume')




urlpatterns_resume = [
    path("api/", include(router.urls)),
]