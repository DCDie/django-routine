from setuptools import setup

version = '1.3.6'

if __name__ == '__main__':
    setup(
        name='django-routine',
        version=version,
        description='A Django app for managing routines.',
        author='Daniel Cuznetov',
        author_email='danielcuznetov04@gmail.com',
        packages=['django_routine'],
        entry_points={
            "console_scripts": [
                "startproject = django_routine.main:main",
            ]
        },
        install_requires=[
            'djangorestframework',
            'django',
            'django-rest-swagger',
            'drf_yasg',
            'djangorestframework-simplejwt',
            'django-filter',
            'faker',
            'gunicorn',
            'psycopg2-binary',
            'django-celery-beat',
            'django-celery-results',
            'python-dotenv',
        ],
    )
