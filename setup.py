from setuptools import setup

version = '0.0.3.0'

setup(
    name='django-rutine',
    version=version,
    description='A Django app for managing routines.',
    author='Daniel Cuznetov',
    author_email='danielcuznetov04@gmail.com',
    packages=['django_rutine'],
    entry_points={
        "console_scripts": [
            "startapp = django_rutine.start:start",

        ]
    },
    install_requires=['djangorestframework', 'django'],
)
