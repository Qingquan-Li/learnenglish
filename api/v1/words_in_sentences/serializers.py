from rest_framework import serializers

from words_in_sentences.models import Tag
from words_in_sentences.models import Sentence


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        # fields = "__all__"
        fields = (
            # 'id',
            'name',
            # 'is_active',
        )


class SentenceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sentence
        fields = (
            'id',
            'created_at',
            # 'modified_at',
            # 'version',
            # 'is_active',
            'english_sentence',
            'highlight_word',
            # 'slug',
            'chinese_translation',
            # 'original_source',
            'note',
            'tags',
            # 'created_by',
            'publish_date',
            'is_understand',
        )


class SentenceDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sentence
        fields = "__all__"
