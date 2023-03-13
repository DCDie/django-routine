import os
import sys
from pathlib import Path
from platform import python_version


class CreateFiles:
    def __init__(self, path=None, name=None):
        self.path = path
        self.name = name

    def create_serializer(self):
        serializer = open(self.path.joinpath('serializers.py'), 'w+')
        serializer.write(
            "from rest_framework import serializers\n\n"
            f"from apps.{self.name}.models import *\n\n\n"
            f"class {self.name.capitalize()}Serializer(serializers.ModelSerializer):\n"
            "    class Meta:\n"
            f"        model = {self.name.capitalize()}\n"
            "        fields = '__all__'\n")

    def create_admin(self):
        admin = open(self.path.joinpath('admin.py'), 'w+')
        admin.write(
            "from django.contrib import admin\n\n"
            f"from apps.{self.name}.models import {self.name.capitalize()}\n\n"
            "from apps.common.admin import get_model_fields\n\n\n"
            f"@admin.register({self.name.capitalize()})\n"
            f"class {self.name.capitalize()}Admin(admin.ModelAdmin):\n"
            "    list_display = get_model_fields\n"
        )

    def create_test(self):
        test = open(self.path.joinpath('tests.py'), 'w+')
        test.write(
            "from django.contrib.auth import get_user_model\n"
            "from django.urls import reverse\n"
            "from django.test import TestCase\n"
            "from faker import Faker\n"
            "from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT\n"
            "from rest_framework_simplejwt.tokens import RefreshToken\n\n"
            f"from apps.{self.name}.models import {self.name.capitalize()}\n\n\n"
            "User = get_user_model()\n"
            "fake = Faker()\n\n\n"
            "def auth(user=None):\n"
            "    refresh = RefreshToken.for_user(user)\n"
            "    return {\n"
            "        'HTTP_AUTHORIZATION': f'Bearer {refresh.access_token}'\n"
            "    }\n\n\n"
            f"class {self.name.capitalize()}Test(TestCase):\n"
            "    def setUp(self) -> None:\n"
            "        self.user = User.objects.create(\n"
            "            username=fake.name(),\n"
            "            password=fake.password(),\n"
            "       )\n\n"
            f"    def test_{self.name}_list(self):\n"
            f"        response = self.client.get(reverse('{self.name}-list'), **auth(user=self.user))\n"
            "        self.assertEqual(response.status_code, HTTP_200_OK)\n\n"
            f"    def test_{self.name}_create(self):\n"
            f"        response = self.client.post(reverse('{self.name}-list'), **auth(user=self.user))\n"
            "        self.assertEqual(response.status_code, HTTP_201_CREATED)\n\n"
            f"    def test_{self.name}_retrieve(self):\n"
            f"        {self.name}_instance = {self.name.capitalize()}.objects.create()\n"
            f"        response = self.client.get(reverse('{self.name}-detail', "
            f"kwargs={{'pk': {self.name}_instance.id}}), **auth(user=self.user))\n"
            "        self.assertEqual(response.status_code, HTTP_200_OK)\n\n"
            f"    def test_{self.name}_update(self):\n"
            f"        {self.name}_instance = {self.name.capitalize()}.objects.create()\n"
            f"        response = self.client.put(reverse('{self.name}-detail', "
            f"kwargs={{'pk': {self.name}_instance.id}}), **auth(user=self.user))\n"
            "        self.assertEqual(response.status_code, HTTP_200_OK)\n\n"
            f"    def test_{self.name}_partial_update(self):\n"
            f"        {self.name}_instance = {self.name.capitalize()}.objects.create()\n"
            f"        response = self.client.patch(reverse('{self.name}-detail', "
            f"kwargs={{'pk': {self.name}_instance.id}}), **auth(user=self.user))\n"
            "        self.assertEqual(response.status_code, HTTP_200_OK)\n\n"
            f"    def test_{self.name}_destroy(self):\n"
            f"        {self.name}_instance = {self.name.capitalize()}.objects.create()\n"
            f"        response = self.client.delete(reverse('{self.name}-detail', "
            f"kwargs={{'pk': {self.name}_instance.id}}), **auth(user=self.user))\n"
            "        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)\n"
        )

    def create_urls(self):
        urls = open(self.path.joinpath('urls.py'), 'w+')
        urls.write(
            "from rest_framework import routers\n\n"
            f"from apps.{self.name}.views import {self.name.capitalize()}ViewSet\n\n"
            f"router = routers.SimpleRouter(trailing_slash=False)\n\n"
            f"router.register(r'{self.name}', {self.name.capitalize()}ViewSet, basename='{self.name}')\n\n"
            "urlpatterns = [\n    *router.urls,\n]\n")

    def create_views(self):
        view = open(self.path.joinpath('views.py'), 'w+')
        view.write(
            "from rest_framework.permissions import IsAuthenticated\n"
            "from rest_framework.viewsets import ModelViewSet\n\n"
            "from apps.common.views import CustomGenericViewSet\n"
            f"from apps.{self.name}.models import {self.name.capitalize()}\n"
            f"from apps.{self.name}.serializers import {self.name.capitalize()}Serializer\n\n\n"
            f"class {self.name.capitalize()}ViewSet(CustomGenericViewSet, ModelViewSet):\n"
            f"    serializer_class = {self.name.capitalize()}Serializer\n"
            f"    queryset = {self.name.capitalize()}.objects.all()\n"
            "    permission_classes = (IsAuthenticated,)\n"
            "    ordering = '-updated_at'\n"
            "    filterset_fields = '__all__'\n"
            "    search_fields = '__all__'\n"
            "    serializers_by_action = {\n"
            "        'default': serializer_class,\n"
            "    }\n"
            "    permission_by_action = {\n"
            "        'default': permission_classes,\n"
            "    }\n"
        )

    def create_model(self):
        model = open(self.path.joinpath('models.py'), 'w+')
        model.write(
            "from django.db import models\n\n"
            "from apps.common.models import BaseModel\n\n\n"
            f"class {self.name.capitalize()}(BaseModel):\n"
            "\tpass\n")

    def create_apps(self):
        os.mkdir(f"apps/{self.name}")
        os.system(f"django-admin startapp {self.name} apps/{self.name}")
        apps = open(self.path.joinpath("apps.py"), "w+")
        apps.write(
            "from django.apps import AppConfig\n\n\n"
            f"class {self.name.capitalize()}Config(AppConfig):\n"
            "    default_auto_field = 'django.db.models.BigAutoField'\n"
            f"    name = 'apps.{self.name}'\n")

    @staticmethod
    def add_common_app():
        os.mkdir("apps/common")
        os.system("django-admin startapp common apps/common")
        apps = open("apps/common/apps.py", "w+")
        apps.write(
            "from django.apps import AppConfig\n\n\n"
            "class CommonConfig(AppConfig):\n"
            "    default_auto_field = 'django.db.models.BigAutoField'\n"
            "    name = 'apps.common'\n")

        models = open("apps/common/models.py", "w+")
        models.write(
            "from django.db import models\n\n\n"
            "class BaseModel(models.Model):\n"
            "    objects = models.Manager()\n"
            "    created_at = models.DateTimeField(auto_now_add=True)\n"
            "    updated_at = models.DateTimeField(auto_now=True)\n\n"
            "    class Meta:\n"
            "        abstract = True\n")
        admin = open("apps/common/admin.py", "w+")
        admin.write(
            "from django.contrib import admin\n\n\n"
            "@property\n"
            "def get_model_fields(class_obj):\n"
            "    return [field.name for field in class_obj.model._meta.get_fields()]\n"
        )
        views = open("apps/common/views.py", "w+")
        views.write(
            "from rest_framework.viewsets import GenericViewSet\n\n"
            "DEFAULT = 'default'\n\n\n"
            "class CustomGenericViewSet(GenericViewSet):\n"
            "    serializers_by_action = {}\n"
            "    permission_by_action = {}\n\n"
            "    def get_serializer_class(self):\n"
            "        if serializer := self.serializers_by_action.get(self.action) or "
            "self.serializers_by_action.get(DEFAULT):\n"
            "            return serializer\n"
            "        return super(CustomGenericViewSet, self).get_serializer_class()\n\n"
            "    def get_permissions(self):\n"
            "        if self.action in self.permission_by_action or DEFAULT in self.permission_by_action:\n"
            "            try:\n"
            "                return [permission() for permission in self.permission_by_action[self.action]]\n"
            "            except KeyError:\n"
            "                return [permission() for permission in self.permission_by_action[DEFAULT]]\n"
            "        return super(CustomGenericViewSet, self).get_permissions()\n"
        )

    @staticmethod
    def create_dockerfile():
        python = python_version()
        with open('Dockerfile', 'w+') as dockerfile:
            dockerfile.write(
                f"FROM python:{python}-slim-buster\n\n"
                "WORKDIR /app\n"
                "EXPOSE 8000\n\n"
                "ENV PYTHONDONTWRITEBYTECODE 1\n"
                "ENV PYTHONUNBUFFERED 1\n\n"
                "COPY . .\n"
                "RUN pip install -r requirements.txt\n\n"
                "CMD [\"gunicorn\", \"config.wsgi:application\", \"-bind\", \"0.0.0.0:8000\"]\n"
            )

    @staticmethod
    def create_docker_compose():
        with open('docker-compose.yml', 'w+') as docker_compose:
            docker_compose.write(
                "version: '3.9'\n\n"
                "volumes:\n"
                "  django_postgres:\n"
                "    name: django_postgres\n"
                "  django_rabbitmq:\n"
                "    name: django_rabbitmq\n\n"
                "services:\n"
                "  postgres:\n"
                "    container_name: config_postgres\n"
                "    hostname: postgres.django.com\n"
                "    image: postgres:latest\n"
                "    environment:\n"
                "      POSTGRES_DB: ${POSTGRES_DB}\n"
                "      POSTGRES_USER: ${POSTGRES_USER}\n"
                "      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}\n"
                "    volumes:\n"
                "      - django_postgres:/var/lib/postgresql/data\n"
                "    ports:\n"
                "      - \"5432:5432\"\n\n"
                "  rabbitmq:\n"
                "    container_name: config_rabbitmq\n"
                "    hostname: rabbitmq.django.com\n"
                "    image: rabbitmq:latest\n"
                "    environment:\n"
                "      RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER}\n"
                "      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASS}\n"
                "      RABBITMQ_DEFAULT_VHOST: ${RABBITMQ_VHOST}\n"
                "    ports:\n"
                "      - \"5672:5672\"\n"
                "      - \"15672:15672\"\n"
                "    volumes:\n"
                "      - django_rabbitmq:/var/lib/rabbitmq\n\n"
                "  django:\n"
                "    container_name: config_django\n"
                "    build:\n"
                "      context: .\n"
                "      dockerfile: Dockerfile\n"
                "    env_file:\n"
                "      - .env\n"
                "    command:\n"
                "      - bash\n"
                "      - -c\n"
                "      - |\n"
                "        python manage.py migrate --noinput\n"
                "        python manage.py collectstatic --no-input\n"
                "        python manage.py runserver 0.0.0.0:8000\n"
                "    ports:\n"
                "      - \"8000:8000\"\n"
                "    depends_on:\n"
                "      - postgres\n"
                "      - rabbitmq\n\n"
                "  celery_beat:\n"
                "      container_name: config_celery_beat\n"
                "      build:\n"
                "        context: .\n"
                "        dockerfile: Dockerfile\n"
                "      env_file:\n"
                "        - .env\n"
                "      command: celery -A config.celery:app beat -l INFO\n"
                "      depends_on:\n"
                "        - postgres\n"
                "        - rabbitmq\n\n"
                "  celery_worker:\n"
                "      container_name: config_celery_worker\n"
                "      build:\n"
                "        context: .\n"
                "        dockerfile: Dockerfile\n"
                "      env_file:\n"
                "        - .env\n"
                "      command: celery -A config.celery:app worker -l INFO\n"
                "      depends_on:\n"
                "        - postgres\n"
                "        - rabbitmq\n"
            )

    @staticmethod
    def create_env():
        with open('.env', 'w+') as local_env:
            local_env.write(
                "SECRET_KEY=\n\n"
                "POSTGRES_HOST=postgres.django.com\n"
                "POSTGRES_PORT=5432\n"
                "POSTGRES_DB=postgres\n"
                "POSTGRES_USER=postgres\n"
                "POSTGRES_PASSWORD=postgres\n\n"
                "RABBITMQ_HOST=rabbitmq.django.com\n"
                "RABBITMQ_PORT=5672\n"
                "RABBITMQ_USER=rabbitmq\n"
                "RABBITMQ_PASS=rabbitmq\n"
                "RABBITMQ_VHOST=rabbitmq\n\n"
            )

    @staticmethod
    def create_celery_file():
        with open("config/celery.py", "w+") as celery_file:
            celery_file.write(
                "import os\n"
                "from time import sleep\n\n"
                "from celery import Celery\n\n"
                "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')\n\n"
                "app = Celery('config')\n"
                "app.config_from_object('django.conf:settings', namespace='CELERY')\n"
                "app.conf.timezone = 'UTC'\n"
                "app.autodiscover_tasks()\n\n\n"
                "@app.task(name='debug_task', bind=True, track_started=True)\n"
                "def debug_task(self, sleep_seconds: int = 0, raise_exception: bool = False):\n"
                "    if sleep_seconds:\n"
                "        sleep(sleep_seconds)\n"
                "    if raise_exception:\n"
                "        raise Exception('Intentional exception')\n"
                "    print(f'Request: {self.request!r}')\n"
            )

    def main(self):
        self.create_apps()
        self.create_serializer()
        self.create_test()
        self.create_admin()
        self.create_model()
        self.create_views()
        self.create_urls()
        self.create_dockerfile()
        self.create_docker_compose()
        self.create_env()
        self.create_celery_file()


class UpdateFiles:

    @staticmethod
    def update_urls():
        urls = open('config/urls.py', 'w+')
        urls.write(
            "from django.contrib import admin\n"
            "from django.urls import path, include\n"
            "from rest_framework import permissions\n"
            "from rest_framework_simplejwt.views import (\n"
            "    TokenObtainPairView, TokenRefreshView, TokenVerifyView\n"
            ")\n"
            "from drf_yasg.views import get_schema_view\n"
            "from drf_yasg import openapi\n\n"
            "schema_view = get_schema_view(\n"
            "    openapi.Info(\n"
            "        title='Project API',\n"
            "        default_version='v1',\n"
            "    ),\n"
            "    public=True,\n"
            "    permission_classes=(permissions.AllowAny,),\n"
            ")\n\n"
            "urlpatterns = [\n"
            "    path('admin/', admin.site.urls),\n"
            "    path('', schema_view.with_ui('swagger', cache_timeout=0),\n"
            "         name='schema-swagger-ui'),\n"
            "    path('jwt/', include([\n"
            "        path('token/', TokenObtainPairView.as_view(), name='token_obtain-pair'),\n"
            "        path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),\n"
            "        path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),\n"
            "    ])),\n"
            "]\n")

    @staticmethod
    def add_installed_apps(apps):
        with open('config/settings.py') as settings:
            data = settings.read()
        settings.close()

        apps_list = data.split('\n')
        for i, _ in enumerate(apps_list):
            if apps_list[i] == "    'django.contrib.staticfiles',":
                for app in apps:
                    apps_list.insert(i + 1, f"    \'{app}\',")
                    i += 1

        with open('config/settings.py', 'w') as settings:
            for line in apps_list:
                settings.write(line + '\n')

    @staticmethod
    def extend_config():
        with open('config/settings.py') as settings:
            data = settings.read()
        settings.close()

        settings_list = data.split('\n')

        for i, _ in enumerate(settings_list):
            if settings_list[i] == "from pathlib import Path":
                settings_list.insert(
                    i + 1,
                    "\nfrom datetime import timedelta\n"
                    "from os import environ\n"
                    "from dotenv import load_dotenv\n\n"
                    "load_dotenv()\n"
                )

            if settings_list[i] == "# SECURITY WARNING: keep the secret key used in production secret!":
                del settings_list[i + 1]
                settings_list.insert(
                    i + 1,
                    "SECRET_KEY = environ.get('SECRET_KEY')\n"
                )

            if settings_list[i] == "DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'":
                settings_list.insert(
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
                    "        'Token': {\n"
                    "            'type': 'apiKey',\n"
                    "            'name': 'Authorization',\n"
                    "            'in': 'header'\n"
                    "        }\n"
                    "    }\n"
                    "}\n"

                )
            if settings_list[i] == "STATIC_URL = 'static/'":
                settings_list.insert(
                    i + 1,
                    "STATIC_ROOT = BASE_DIR.joinpath('static')\n\n"
                    "MEDIA_URL = '/media/'\n"
                    "MEDIA_ROOT = BASE_DIR.joinpath('media')\n"
                )
            if settings_list[i] == "DATABASES = {":
                del settings_list[i + 2: i + 4]
                settings_list.insert(
                    i + 2,
                    "        'ENGINE': 'django.db.backends.postgresql',\n"
                    "        'HOST': environ.get('POSTGRES_HOST'),\n"
                    "        'PORT': environ.get('POSTGRES_PORT'),\n"
                    "        'NAME': environ.get('POSTGRES_DB'),\n"
                    "        'USER': environ.get('POSTGRES_USER'),\n"
                    "        'PASSWORD': environ.get('POSTGRES_PASSWORD'),"
                )
            if settings_list[i] == "USE_TZ = True":
                settings_list.insert(
                    i + 2,
                    "RABBITMQ_HOST = environ.get('RABBITMQ_HOST')\n"
                    "RABBITMQ_PORT = environ.get('RABBITMQ_PORT')\n"
                    "RABBITMQ_USER = environ.get('RABBITMQ_USER')\n"
                    "RABBITMQ_PASS = environ.get('RABBITMQ_PASS')\n"
                    "RABBITMQ_VHOST = environ.get('RABBITMQ_VHOST')\n\n"
                    "CELERY_BROKER_URL = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:"
                    "{RABBITMQ_PORT}/{RABBITMQ_VHOST}'\n\n"
                    "CELERY_RESULT_BACKEND = 'django-db'\n\n"
                    "CELERY_RESULT_EXTENDED = True\n\n"
                    "CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'\n"
                )
        with open('config/settings.py', 'w') as settings:
            for line in settings_list:
                settings.write(line + '\n')

    @staticmethod
    def add_urls(apps):
        with open('config/urls.py') as urls:
            data = urls.read()
        urls.close()

        urls_list = data.split('\n')

        for i, _ in enumerate(urls_list):
            if urls_list[i] == 'urlpatterns = [':
                for app in apps:
                    urls_list.insert(
                        i + 1,
                        f"    path('{app.split('.')[-1]}/', include('{app}.urls')),"
                    )
                    i += 1

        with open('config/urls.py', 'w') as urls:
            for line in urls_list:
                urls.write(line + '\n')

    @staticmethod
    def update_config_init():
        with open('config/__init__.py', 'w+') as config:
            config.write(
                "__all__ = ['celery_app']\n\n"
                "from config.celery import app as celery_app\n"
            )


def start():
    os.system('django-admin startproject config .')
    os.system('pip freeze > requirements.txt')
    os.makedirs('apps', exist_ok=True)
    open("apps/__init__.py", "w+").close()
    standard = [
        'rest_framework',
        'drf_yasg',
        'rest_framework_swagger',
        'rest_framework_simplejwt',
        'django_filters',
        'django_celery_beat',
        'django_celery_results',
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
    UpdateFiles().update_config_init()
    os.system('echo All is done, my Captain!')
