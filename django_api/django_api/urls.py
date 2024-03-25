from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from customers.urls import urlpatterns_customers
from users_resume.urls import urlpatterns_resume
from users_work.urls import urlpatterns_work
from webchat.urls import websocket_urlpatterns_webchat

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    # path('verification/', include('verify_email.urls')),

] + urlpatterns_customers + urlpatterns_resume + urlpatterns_work

websocket_urlpatterns = [

] + websocket_urlpatterns_webchat


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
