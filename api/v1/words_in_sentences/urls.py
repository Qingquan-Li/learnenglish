from django.urls import path
from .views import SentenceList, SentenceDetail
from .views import TagList, TagDetail

# docs.djangoproject.com/en/3.2/intro/tutorial03/#namespacing-url-names
app_name = 'api_v1_words_in_sentences'

urlpatterns = [
    path('sentences/', SentenceList.as_view(), name='sentence-list'),
    path('sentences/<int:pk>/', SentenceDetail.as_view(), name='sentence-detail'),
    path('tags/', TagList.as_view(), name='tag-list'),
    path('tags/<int:pk>/', TagDetail.as_view(), name='tag-detail'),
]
