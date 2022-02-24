from django.urls import path
from . import views

# docs.djangoproject.com/en/3.2/intro/tutorial03/#namespacing-url-names
app_name = 'writing'

urlpatterns = [
    # path('', views.ArticleList.as_view(), name='article-list'),
    # path('writing/<int:pk>/', views.article_detail, name='article-detail'),
    # # stackoverflow.com/questions/31003934
    # path(
    #     'writing/<int:pk>/<slug:slug>',
    #     views.article_detail,
    #     name='article-detail-with-slug'
    # ),
    # path('writing/search/', views.search, name="search"),
]
