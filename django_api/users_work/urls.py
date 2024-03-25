from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers


from users_work import views

router = routers.DefaultRouter()
router.register(r'userwork', views.WorkViewSet, basename='userwork')




urlpatterns_work = [
    path("api/", include(router.urls)),
]