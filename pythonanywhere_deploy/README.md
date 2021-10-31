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

<br>

---

<br>

# Before deploying new code to PythonAnywhere

## 1. Deployment checklist
> References:
> https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

```bash
$ python manage.py check --deploy [--settings=...]
```

## 2. Managing static files
> References:
> https://docs.djangoproject.com/en/3.2/howto/static-files/#deployment

If you hava added new static files (e.g. images, JavaScript, CSS),
you should run the `collectstatic` management command:

```bash
$ python manage.py collectstatic [--settings=...]
```

## 3. Migrations
> References:
> https://docs.djangoproject.com/en/3.2/topics/migrations/

If you have changed the models' fields or added/deleted models,
you should run the command:

```bash
# Creating new migrations based on models:
$ python manage.py makemigrations [app_name] --settings=a_project_config.settings.local

# Applying migrations to database:
$ python manage.py migrate --settings=a_project_config.settings.local
```

## 4. Managing package dependencies

If you hava added new package dependencies, you should run the command
to record an environment's current package list into requirements.txt:

```bash
$ pip freeze > requirements.txt
```

## 5. Running the test code
```bash
$ python manage.py test --settings=a_project_config.settings.local
```

## 6. Pushing new code to GitHub
> References:
> https://github.com/git-guides/git-push

```bash
$ git add .
$ git commit -m "descriptive message"
$ git push
```

<br>

---

<br>

# Deploying new code to PythonAnywhere

## 1. Entering the project path and activating the virtual environment
```bash
$ cd learnenglish && source venv/bin/activate
```

## 2. Pulling new code from GitHub
> References:
> https://github.com/git-guides/git-pull

```bash
$ git pull # or: git fetch + git merge
```

## 3. Installing package dependencies

If you hava added new package dependencies,
you should run the command to intall them:

```bash
$ pip install -r requirements.txt
```

## 4. Applying migrations to database:

If you have changed the models' fields or added/deleted models,
you should run the command:

```bash
$ python manage.py migrate --settings=a_project_config.settings.production
```

## 5. Running the test code
```bash
$ python manage.py test --settings=a_project_config.settings.production
```

Note: Cannot run the test code that depends on the database
since we use MySQL provided by PythonAnywhere:

```bash
$ python manage.py test --settings=a_project_config.settings.production
Creating test database for alias 'default'...
Got an error creating the test database: (1044, "Access denied for user 'jakeli'@'%' to database 'test_jakeli$learnenglish'")
```

## 6. Reloading the web app on PythonAnywhere
Click the `Reload` button on PythonAnywhere
