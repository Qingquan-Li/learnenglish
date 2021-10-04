# Deploying an existing Django project on PythonAnywhere

> Reference:
> https://help.pythonanywhere.com/pages/DeployExistingDjangoProject

1. Pull code from GitHub: https://github.com/FatliTalk/learnenglish
2. Create a virtual environment and Install requirements
    - `$ python3.9 -m venv venv`
    - `$ pip install -r requirements.txt`
3. Create a Web app with Manual Configuration and Enter the virtual environment path
4. Edit the WSGI configuration file
    ```python
    # /var/www/jakeli_pythonanywhere_com_wsgi.py

    import os
    import sys

    # Assuming you use python-dotenv
    # https://help.pythonanywhere.com/pages/environment-variables-for-web-apps/
    from dotenv import load_dotenv
    project_folder = os.path.expanduser('~/learnenglish')
    load_dotenv(os.path.join(project_folder, '.env'))

    # assuming your django settings file is at
    # '/home/jakeli/learnenglish/a_project_config/settings/production.py'
    # and your manage.py is is at '/home/jakeli/learnenglish/manage.py'
    path = '/home/jakeli/learnenglish'
    if path not in sys.path:
        sys.path.append(path)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'a_project_config.settings.production'

    # then:
    from django.core.wsgi import get_wsgi_application  # noqa
    application = get_wsgi_application()
    ```
5. Configure MySQL database
    1. Usage of PythonAnywhere MySQL: https://help.pythonanywhere.com/pages/UsingMySQL
    2. Applying migrations to database:
        `$ python manage.py migrate --settings=a_project_config.settings.production`
    3. Creating an admin user:
        `$ python manage.py createsuperuser --settings=a_project_config.settings.production`
