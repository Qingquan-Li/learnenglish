# 1. Creating custom User model

> References：
> docs.djangoproject.com/en/3.2/topics/auth/customizing/#substituting-a-custom-user-model

Creating the custom User model and point AUTH_USER_MODEL to it in `settings` file
before creating any migrations or running manage.py migrate for the first time.

<br>

### Note:
> References：
> https://stackoverflow.com/questions/44651760/

If you have executed the first `$ python manage.py migrate` command
after initializing the Django project and before creating a custom user model:

1. Delete the _pycache_ and the 0001_initial files.
2. Delete the db.sqlite3 from the root directory.
3. Rerun: $ python manage.py makemigrations and $ python manage.py migrate

<br>

# 2. Database table changes

```bash
$ sqlite3 './db.sqlite3'
SQLite version 3.32.3 2020-06-18 14:16:19
Enter ".help" for usage hints.
sqlite> .table
accounts_customuser                   auth_permission
accounts_customuser_groups            django_admin_log
accounts_customuser_user_permissions  django_content_type
auth_group                            django_migrations
auth_group_permissions                django_session
```

The default original database table:
```bash
auth_group                  auth_user_user_permissions
auth_group_permissions      django_admin_log
auth_permission             django_content_type
auth_user                   django_migrations
auth_user_groups            django_session
```
