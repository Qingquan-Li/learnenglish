from django.test import TestCase

from writing.models import Article, Tag


class ArticleModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.article = Article.objects.create(
            # id,
            # created_time,
            # modified_time,
            # version,
            # is_active,
            title='The First Article',
            slug='the-first-article',
            summary='This is the summary of the first article.',
            body='After the first enumeration, required by the first article of the Constitution...',
            # tags,
            # author,
        )

    def test_version_content(self) -> None:
        expected_object_name = f'{self.article.version}'
        self.assertEqual(expected_object_name, '1')

    def test_is_active(self) -> None:
        self.assertTrue(self.article.is_active)

    def test_title_content(self) -> None:
        expected_object_name = f'{self.article.title}'
        self.assertEqual(expected_object_name, 'The First Article')

    def test_slug_content(self) -> None:
        expected_object_name = f'{self.article.slug}'
        self.assertEqual(expected_object_name, 'the-first-article')

    def test_summary_content(self) -> None:
        expected_object_name = f'{self.article.summary}'
        self.assertEqual(expected_object_name, 'This is the summary of the first article.')

    def test_body_content(self) -> None:
        expected_object_name = f'{self.article.body}'
        self.assertEqual(
            expected_object_name,
            'After the first enumeration, required by the first article of the Constitution...'
        )

    def test_get_absolute_url(self) -> None:
        # This will also fail if the urlconf is not defined.
        self.assertEqual(
            self.article.get_absolute_url(),
            '/writing/{id}/{slug}'.format(id=self.article.pk, slug=self.article.slug)
        )


class TagModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.tag = Tag.objects.create(
            # id,
            name='First Tag',
            is_active=0,
        )

    def test_name_content(self) -> None:
        expected_object_name = f'{self.tag.name}'
        self.assertEqual(expected_object_name, 'First Tag')

    def test_is_active(self) -> None:
        self.assertFalse(self.tag.is_active)


"""
$ python manage.py test writing.tests.test_models --settings=a_project_config.settings.local
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.........
----------------------------------------------------------------------
Ran 9 tests in 0.015s

OK
Destroying test database for alias 'default'...
"""
