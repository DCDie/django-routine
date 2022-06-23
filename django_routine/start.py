import os
import sys
from pathlib import Path


class CreateFiles:
    def __init__(self, path=None, name=None):
        self.path = path
        self.name = name

    def create_serializer(self):
        serializer = open(self.path.joinpath('serializers.py'), 'w+')
        serializer.write(
            f"from rest_framework import serializers\n"
            f"from apps.{self.name}.models import *\n\n\n"
            f"class {self.name.capitalize()}Serializer(serializers.ModelSerializer):\n"
            f"    class Meta:\n"
            f"        model = {self.name.capitalize()}\n"
            f"        fields = '__all__'\n")

    def create_urls(self):
        urls = open(self.path.joinpath('urls.py'), 'w+')
        urls.write(
            f"from rest_framework import routers\n"
            f"from apps.{self.name}.views import {self.name.capitalize()}ViewSet\n\n"
            f"router = routers.SimpleRouter(trailing_slash=False)\n\n\n"
            f"router.register(r'{self.name}', {self.name.capitalize()}ViewSet, basename='{self.name}')\n\n"
            f"urlpatterns = [\n    *router.urls,\n]\n")

    def create_views(self):
        view = open(self.path.joinpath('views.py'), 'w+')
        view.write(
            f"from rest_framework.viewsets import ModelViewSet\n\n"
            f"from apps.{self.name}.models import {self.name.capitalize()}\n"
            f"from apps.{self.name}.serializers import {self.name.capitalize()}Serializer\n\n\n"
            f"class {self.name.capitalize()}ViewSet(ModelViewSet):\n"
            f"    serializer_class = {self.name.capitalize()}Serializer\n"
            f"    queryset = {self.name.capitalize()}.objects.all()\n"
            f"    ordering = '-updated_at'\n"
            f"    filterset_fields = '__all__'\n"
            f"    search_fields = '__all__'\n"
        )

    def create_model(self):
        model = open(self.path.joinpath('models.py'), 'w+')
        model.write(
            f"from django.db import models\n\n"
            f"from apps.common.models import BaseModel\n\n\n"
            f"class {self.name.capitalize()}(BaseModel):\n"
            f"    pass\n")

    def create_apps(self):
        os.mkdir(f"apps/{self.name}")
        os.system(f"django-admin startapp {self.name} apps/{self.name}")
        apps = open(self.path.joinpath("apps.py"), "w+")
        apps.write(
            f"from django.apps import AppConfig\n\n\n"
            f"class {self.name.capitalize()}Config(AppConfig):\n"
            f"    default_auto_field = 'django.db.models.BigAutoField'\n"
            f"    name = 'apps.{self.name}'\n")

    def add_common_app(self):
        os.mkdir("apps/common")
        os.system("django-admin startapp common apps/common")
        apps = open("apps/common/apps.py", "w+")
        apps.write(
            f"from django.apps import AppConfig\n\n\n"
            f"class CommonConfig(AppConfig):\n"
            f"    default_auto_field = 'django.db.models.BigAutoField'\n"
            f"    name = 'apps.common'\n")

        models = open("apps/common/models.py", "w+")
        models.write(
            "from django.db import models\n\n\n"
            "class BaseModel(models.Model):\n"
            "    created_at = models.DateTimeField(auto_now_add=True)\n"
            "    updated_at = models.DateTimeField(auto_now=True)\n\n"
            "    class Meta:\n"
            "        abstract = True\n")

    def main(self):
        self.create_apps()
        self.create_serializer()
        self.create_model()
        self.create_views()
        self.create_urls()


class UpdateFiles:
    def __init__(self, path=None, name=None):
        self.path = path
        self.name = name

    def update_urls(self):
        urls = open('config/urls.py', 'w+')
        urls.write(
            f"from django.contrib import admin\n"
            f"from django.urls import path, include\n"
            f"from rest_framework import permissions\n"
            f"from rest_framework_simplejwt.views import (\n"
            f"    TokenObtainPairView, TokenRefreshView, TokenVerifyView\n"
            f")\n"
            f"from drf_yasg.views import get_schema_view\n"
            f"from drf_yasg import openapi\n\n"
            f"schema_view = get_schema_view(\n"
            f"    openapi.Info(\n"
            f"        title='Project API',\n"
            f"        default_version='v1',\n"
            f"    ),\n"
            f"    public=True,\n"
            f"    permission_classes=(permissions.AllowAny,),\n"
            f")\n\n"
            f"urlpatterns = [\n"
            f"    path('admin/', admin.site.urls),\n"
            f"    path('', schema_view.with_ui('swagger', cache_timeout=0),\n"
            f"         name='schema-swagger-ui'),\n"
            f"    path('jwt/', include([\n"
            f"        path('token/', TokenObtainPairView.as_view(), name='token_obtain-pair'),\n"
            f"        path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),\n"
            f"        path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),\n"
            f"    ])),\n"
            f"]\n")

    def add_installed_apps(self, apps):
        with open('config/settings.py') as settings:
            data = settings.read()
        settings.close()

        list = data.split('\n')
        for i in range(len(list)):
            if list[i] == "    'django.contrib.staticfiles',":
                for app in apps:
                    list.insert(i + 1, f"    \'{app}\',")
                    i += 1

        with open('config/settings.py', 'w') as settings:
            for line in list:
                settings.write(line + '\n')

    def extend_config(self):
        with open('config/settings.py') as settings:
            data = settings.read()
        settings.close()

        list = data.split('\n')

        for i in range(len(list)):
            if list[i] == "from pathlib import Path":
                list.insert(i + 1, "\nfrom datetime import timedelta\n")

            if list[i] == "DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'":
                list.insert(
                    i + 2,
                    "REST_FRAMEWORK = {\n"
                    "    'DEFAULT_AUTHENTICATION_CLASSES': (\n"
                    "        'rest_framework_simplejwt.authentication.JWTAuthentication',\n"
                    "        'rest_framework.authentication.SessionAuthentication',\n"
                    "    ),\n"
                    "    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',\n"
                    "    'PAGE_SIZE': 20,\n"
                    "    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend',\n"
                    "                                'rest_framework.filters.SearchFilter',\n"
                    "                                'rest_framework.filters.OrderingFilter',\n"
                    "                                ],\n"
                    "}\n\n\n"
                    "SIMPLE_JWT = {\n"
                    "    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),\n"
                    "    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),\n"
                    "    'AUTH_HEADER_TYPES': ('Bearer',),\n"
                    "    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',\n"
                    " }\n\n\n"
                    "SWAGGER_SETTINGS = {\n"
                    "    'SECURITY_DEFINITIONS': {\n"
                    "         'Token': {\n"
                    "            'type': 'apiKey',\n"
                    "            'name': 'Authorization',\n"
                    "            'in': 'header'\n"
                    "        }\n"
                    "    }\n"
                    "}\n"

                )
        with open('config/settings.py', 'w') as settings:
            for line in list:
                settings.write(line + '\n')

    def add_urls(self, apps):

        with open('config/urls.py') as urls:
            data = urls.read()
        urls.close()

        list = data.split('\n')

        for i in range(len(list)):
            if list[i] == 'urlpatterns = [':
                for app in apps:
                    list.insert(
                        i + 1,
                        f"    path('{app.split('.')[-1]}/', include('{app}.urls')),"
                    )
                    i += 1

        with open('config/urls.py', 'w') as urls:
            for line in list:
                urls.write(line + '\n')


def start():
    os.system('django-admin startproject config .')
    os.mkdir('apps')
    standard = [
        'rest_framework',
        'drf_yasg',
        'rest_framework_swagger',
        'rest_framework_simplejwt',
        'django_filters',
        'apps.common'
    ]
    apps = []
    UpdateFiles().update_urls()
    CreateFiles().add_common_app()
    if len(sys.argv):
        for arg in sys.argv:
            if arg != sys.argv[0]:
                path = Path('apps').absolute().joinpath(arg)
                CreateFiles(path=path, name=arg).main()
                apps.append(f"apps.{arg}")
    UpdateFiles().add_installed_apps([*standard, *apps])
    UpdateFiles().extend_config()
    UpdateFiles().add_urls(apps)
    os.system('echo All is done, my Captain!')
