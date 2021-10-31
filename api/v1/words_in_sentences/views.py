from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions

from words_in_sentences.models import Sentence
from words_in_sentences.models import Tag
from .serializers import SentenceListSerializer, SentenceDetailSerializer
from .serializers import TagSerializer
from .utils.permissions import IsSentenceCreatorOrReadOnly
from .utils.pagination import CustomSentencePagination, CustomTagPagination


# https://www.django-rest-framework.org/api-guide/generic-views/
class SentenceList(generics.ListCreateAPIView):
    queryset = Sentence.objects.all()
    serializer_class = SentenceListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CustomSentencePagination

    # override the create function by changing the response structure
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(
            {
                'status': 'ok',
                'message': 'Sentence Added!',
                'data': serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class SentenceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SentenceDetailSerializer
    permission_classes = (IsSentenceCreatorOrReadOnly,)

    # https://docs.djangoproject.com/en/3.2/topics/db/queries/#caching-and-querysets
    # queryset = Sentence.objects.all()
    # If you are overriding a view method, it is important that you call `get_queryset()`
    # instead of accessing the `queryset` property directly, as `queryset` will get
    # evaluated only once, and those results are cached for all subsequent requests.
    def get_queryset(self):
        return Sentence.objects.filter(id=self.kwargs.get('pk', None))

    # change the response structure for the PUT operation
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        # return Response(serializer.data)
        return Response({'status': 'ok', 'message': 'Sentence Updated!', 'data': serializer.data})


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CustomTagPagination


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAdminUser,)
