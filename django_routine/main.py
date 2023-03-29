import os
import sys
from pathlib import Path

from .create_files import CreateFiles
from .update_files import UpdateFiles


def main():
    # Create a new Django project in the current directory
    os.system('django-admin startproject config .')

    # Save a list of installed packages to requirements.txt
    os.system('pip freeze > requirements.txt')

    # Create a directory for the custom apps and an empty __init__.py file
    os.makedirs('apps', exist_ok=True)
    Path('apps/__init__.py').touch()

    # Define a list of standard packages and an empty list for custom apps
    third_party_apps = [
        'rest_framework',
        'drf_yasg',
        'rest_framework_swagger',
        'rest_framework_simplejwt',
        'django_filters',
        'django_celery_beat',
        'django_celery_results',
    ]
    local_apps = [
        'apps.common',
    ]

    # Update the project's URLs file and add a common app
    UpdateFiles().update_urls()
    CreateFiles().add_common_app()

    # Add any custom apps specified as command-line arguments
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            # Create a directory for the app and generate its files
            app_path = Path('apps').joinpath(arg)
            CreateFiles(path=app_path, name=arg).main()
            local_apps.append(f"apps.{arg}")

    # Update various files with the list of installed apps
    UpdateFiles().add_installed_apps(third_party_apps, local_apps)
    UpdateFiles().extend_config()
    UpdateFiles().add_urls(local_apps)
    UpdateFiles().update_config_init()

    # Print a completion message
    print('All done, Captain!')
