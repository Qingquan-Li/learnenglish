# Before deploying new code to Server

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

## 7. Transferring environment variables (`.env`) to server
> References:
> https://saurabh-kumar.com/python-dotenv/

```bash
$ cd project_directory # Local
$ sftp username@server_ip
$ cd project_directory # Server
$ put .env # Transferring Local Files to the Remote System
```

<br>

---

<br>

# Deploying new code to Server

## 1. Entering the project path and activating the virtual environment
```bash
$ cd ~/learnenglish && source .venv/bin/activate
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
(.venv) $ pip install -r requirements.txt
```

## 4. Applying migrations to database:

If you have changed the models' fields or added/deleted models,
you should run the command:

```bash
(.venv) $ python manage.py migrate --settings=a_project_config.settings.production
```

## 5. Running the test code
```bash
(.venv) $ python manage.py test --settings=a_project_config.settings.production
# If 'permission denied  to create database', run:
# $ sudo -u postgres psql
# postgres=# \du  \\ -- to list all users
# postgres=# ALTER USER your-postgres-user-name WITH SUPERUSER;
```

## 6. Restart Gunicorn and Nginx

> To read more, please check deploy/gunicorn-config.md and deploy/nginx-config.md

```bash
$ sudo systemctl restart gunicorn
$ sudo systemctl restart nginx
```
