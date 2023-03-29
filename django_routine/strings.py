CONFIG_URLS = """from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

get_schema_view(
    openapi.Info(
        title='Project API',
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jwt/', include([
        path('token/', TokenObtainPairView.as_view(), name='token_obtain-pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
        path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    ])),
]"""
CONFIG_INIT = """__all__ = ['celery_app']

from config.celery import app as celery_app
"""
CREATE_SERIALIZERS = """from rest_framework import serializers

from apps.{name}.models import *


class {capitalized_name}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {capitalized_name}
        fields = '__all__'
"""