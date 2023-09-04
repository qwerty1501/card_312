from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .yasg import urlpatterns as doc_urls
from . import settings
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('api/token/access/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('admin/', admin.site.urls),
    path('', include('apps.categories.urls')),
    path('', include('apps.users.urls')),
    path('', include('apps.service.urls')),
    path('', include('apps.event.urls')),
]

urlpatterns += doc_urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)