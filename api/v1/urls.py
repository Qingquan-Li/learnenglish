from django.urls import path
from django.urls import include

urlpatterns = [
    path('words-in-sentences/', include('api.v1.words_in_sentences.urls')),
]
