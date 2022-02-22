from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# docs.djangoproject.com/en/3.2/intro/tutorial03/#namespacing-url-names
app_name = 'words_in_sentences'

urlpatterns = [
    # Set words-in-sentences as the homepage.
    path('', views.SentenceList.as_view(), name='sentence-list'),
    path('words-in-sentences/', views.SentenceList.as_view(), name='sentence-list'),
    path('words-in-sentences/<int:pk>/', views.sentence_detail, name='sentence-detail'),
    path('words-in-sentences/search/', views.search, name="search"),
]
