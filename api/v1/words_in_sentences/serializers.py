from rest_framework import serializers

from words_in_sentences.models import Tag
from words_in_sentences.models import Sentence


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        # fields = (
        #     # 'id',
        #     'name',
        #     'is_active',
        # )
        fields = "__all__"


class SentenceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sentence
        fields = (
            'id',
            'created_time',
            # 'modified_time',
            # 'version',
            'is_active',
            'english_sentence',
            'highlight_word',
            # 'slug',
            'chinese_translation',
            # 'original_source',
            'note',
            'tags',
            # 'author',
            'publish_date',
        )


class SentenceDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sentence
        fields = "__all__"
