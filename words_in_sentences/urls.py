from django.urls import path
from . import views

# docs.djangoproject.com/en/3.2/intro/tutorial03/#namespacing-url-names
app_name = 'words_in_sentences'

urlpatterns = [
    # Set words-in-sentences as the homepage.
    path('', views.SentenceList.as_view(), name='sentence-list'),
    path('words-in-sentences/', views.SentenceList.as_view(), name='sentence-list'),
    path('words-in-sentences/<int:pk>/', views.sentence_detail, name='sentence-detail'),
    # stackoverflow.com/questions/31003934
    path('words-in-sentences/<int:pk>/<slug:slug>', views.sentence_detail, name='sentence-detail-with-slug'),
    path('words-in-sentences/search/', views.search, name="search"),
]
