from django.test import TestCase

from words_in_sentences.models import Sentence
from words_in_sentences.models import Tag


class SentenceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        Sentence.objects.create(
            # id,
            # created_at,
            # modified_at,
            # version,
            # is_active,
            english_sentence='first english sentence',
            highlight_word='english',
            slug='english',
            chinese_translation='第一个英文句子',
            original_source='http://example.com/',
            note='english: /ˈiNG(ɡ)liSH/  [Noun] 英语，英国人  [Verb] 英国化  [Adjective] 英国人的',
            # tags,
            # created_by,
            # publish_date,
            # is_understand,
        )

    def test_version_content(self) -> None:
        sentence = Sentence.objects.get(id=1)
        expected_object_name = f'{sentence.version}'
        self.assertEqual(expected_object_name, '1')
    
    def test_is_active(self) -> None:
        sentence = Sentence.objects.get(id=1)
        self.assertTrue(sentence.is_active)

    def test_english_sentence_content(self) -> None:
        sentence = Sentence.objects.get(id=1)
        expected_object_name = f'{sentence.english_sentence}'
        self.assertEqual(expected_object_name, 'first english sentence')

    def test_highlight_word_content(self) -> None:
        sentence = Sentence.objects.get(id=1)
        expected_object_name = f'{sentence.highlight_word}'
        self.assertEqual(expected_object_name, 'english')

    def test_chinese_translation_content(self) -> None:
        sentence = Sentence.objects.get(id=1)
        expected_object_name = f'{sentence.chinese_translation}'
        self.assertEqual(expected_object_name, '第一个英文句子')

    def test_note_content(self) -> None:
        sentence = Sentence.objects.get(id=1)
        expected_object_name = f'{sentence.note}'
        self.assertEqual(
            expected_object_name,
            'english: /ˈiNG(ɡ)liSH/  [Noun] 英语，英国人  [Verb] 英国化  [Adjective] 英国人的'
        )

    def test_get_absolute_url(self):
        sentence = Sentence.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(
            sentence.get_absolute_url(), '/api/v1/words-in-sentences/sentences/1/')


class TagModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        Tag.objects.create(
            # id,
            name='first tag',
            is_active=0,  # or is_active='0',
        )

    def test_name_content(self) -> None:
        tag = Tag.objects.get(id=1)
        expected_object_name = f'{tag.name}'
        self.assertEqual(expected_object_name, 'first tag')

    def test_is_active(self) -> None:
        tag = Tag.objects.get(id=1)
        self.assertFalse(tag.is_active)

    def test_get_absolute_url(self):
        tag = Tag.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(
            tag.get_absolute_url(), '/api/v1/words-in-sentences/tags/1/')


"""
$ python manage.py test words_in_sentences.tests.test_models --settings=a_project_config.settings.local
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..........
----------------------------------------------------------------------
Ran 10 tests in 0.016s

OK
Destroying test database for alias 'default'...
"""
