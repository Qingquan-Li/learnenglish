from django.urls import path
from . import views

# docs.djangoproject.com/en/3.2/intro/tutorial03/#namespacing-url-names
app_name = 'speech'

urlpatterns = [
    path('', views.ArticleList.as_view(), name='speech-article-list'),
    path('<int:pk>/', views.article_detail, name='speech-article-detail'),
    # stackoverflow.com/questions/31003934
    path(
        '<int:pk>/<slug:slug>',
        views.article_detail,
        name='speech-article-detail-with-slug'
    ),
    path('search/', views.search, name="speech-article-search"),
]
