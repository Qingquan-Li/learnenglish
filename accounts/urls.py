from django.urls import path
from django.contrib.auth import views as auth_views

# docs.djangoproject.com/en/3.2/intro/tutorial03/#namespacing-url-names
app_name = 'accounts'

urlpatterns = [
    # docs.djangoproject.com/en/3.2/topics/auth/default/#module-django.contrib.auth.views
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='/'),
        name='logout'
    ),
]
