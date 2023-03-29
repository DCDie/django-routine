from typing import List

from .strings import CONFIG_URLS, CONFIG_INIT


class UpdateFiles:

    @staticmethod
    def update_urls():
        # Create urls.py file and add the new app urls
        urls = open('config/urls.py', 'w+')
        urls.write(CONFIG_URLS)

    @staticmethod
    def add_installed_apps(third_party_apps: List[str], local_apps: List[str]):
        # Read the content of the settings.py file
        with open('config/settings.py') as f:
            content = f.read()

        # Find the start and end of the 'INSTALLED_APPS' section
        start_index = content.find('INSTALLED_APPS') + 19
        end_index = content.find(']', start_index) - 1

        # Extract the current INSTALLED_APPS
        current_apps = content[start_index:end_index].split('\n')

        # Create the new INSTALLED_APPS
        third_party_apps_list = []
        local_apps_list = []

        third_party_apps_list += [f"    '{app}'," for app in third_party_apps]
        local_apps_list += [f"    '{app}'," for app in local_apps]

        # Combine the new content and write it back to the file
        new_content = content[:start_index] + \
                      '    # Django apps\n' + '\n'.join(current_apps) + '\n' + \
                      '    # Third-party apps\n' + '\n'.join(third_party_apps_list) + '\n' + \
                      '    # Local apps\n' + '\n'.join(local_apps_list) + \
                      content[end_index:]
        with open('config/settings.py', 'w') as f:
            f.write(new_content)

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
        # It opens the "__init__.py" file and overwrites it.
        with open('config/__init__.py', 'w+') as config:
            config.write(CONFIG_INIT)
