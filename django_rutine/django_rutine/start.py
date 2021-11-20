import os
import sys
from pathlib import Path


class CreateFile:
    def __init__(self, path=None, name=None):
        self.path = path
        self.name = name

    def start_serializer(self):
        serializer = open(self.path.joinpath('serializers.py'), 'w+')
        serializer.write(f"from rest_framework import serializers\n"
                         f"from apps.{self.name}.models import *\n\n\n"
                         f"class {self.name.capitalize()}Serializer(serializers.ModelSerializer):\n"
                         f"    class Meta:\n"
                         f"        model = {self.name.capitalize()}\n"
                         f"        fields = '__all__'\n")

    def start_urls(self):
        open(self.path.joinpath('urls.py'), 'w+').close()

    def start_views(self):
        view = open(self.path.joinpath('views.py'), 'w+')
        view.write(f'from rest_framework.viewsets import GenericViewSet\n\n\nclass {self.name.capitalize()}ViewSet('
                   f'GenericViewSet):\n    pass\n')

    def start_model(self):
        model = open(self.path.joinpath('models.py'), 'w+')
        model.write(f'from django.db import models\n\n\n'
                    f'class {self.name.capitalize()}(models.Model):\n'
                    f'    created_at = models.DateTimeField(auto_now_add=True)\n'
                    f'    updated_at = models.DateTimeField(auto_now=True)\n\n'
                    f'    class Meta:\n'
                    f'        abstract = True\n')

    def start_app(self):
        os.mkdir(f'apps/{self.name}')
        os.system(f'django-admin startapp {self.name} apps/{self.name}')
        self.start_serializer()
        self.start_model()
        self.start_views()
        self.start_urls()


def start():
    os.system('django-admin startproject config .')
    os.mkdir('apps')
    if len(sys.argv):
        for arg in sys.argv:
            if arg != sys.argv[0]:
                path = Path('apps').absolute().joinpath(arg)
                CreateFile(path=path, name=arg).start_app()
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')
    os.system('python manage.py runserver')
