from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from words_in_sentences.models import Sentence
from words_in_sentences.models import Tag


class SentenceViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='Jake',
            password='testpass123'
        )

    def test_list_sentences(self):
        """ List (get) all sentences object. """
        Sentence.objects.create(
            english_sentence='First english sentence',
        )
        url = reverse('api_v1_words_in_sentences:sentence-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data[0]['english_sentence'], 'First english sentence')
        # with pagination:
        self.assertEqual(
            response.data['results'][0]['english_sentence'],
            'First english sentence'
        )

    def test_create_sentence(self):
        """ Create (post) a new sentence object. """
        # The self.client attribute will be an APIClient
        # (instead of Django's default Client) instance.
        self.client.login(
            username=self.user.username,
            password='testpass123'
        )
        url = reverse('api_v1_words_in_sentences:sentence-list')
        data = {'english_sentence': 'Second english sentence'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sentence.objects.count(), 1)
        self.assertEqual(Sentence.objects.get().english_sentence, 'Second english sentence')

    def test_create_sentence_not_login(self):
        """ Not login, can not Create (post) a new sentence object. """
        url = reverse('api_v1_words_in_sentences:sentence-list')
        data = {'english_sentence': 'An english sentence'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_sentence(self):
        """ Retrieve (get) a sentence object. """
        sentence = Sentence.objects.create(
            english_sentence='Third english sentence',
        )
        response = self.client.get(
            reverse('api_v1_words_in_sentences:sentence-detail', args=(sentence.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response.data.english_sentence:
        # AttributeError: 'ReturnDict' object has no attribute 'english_sentence'
        self.assertEqual(response.data['english_sentence'], 'Third english sentence')

    def test_update_sentence(self):
        """ Update (put) a sentence object. """
        # The self.client attribute will be an APIClient
        # (instead of Django's default Client) instance.
        self.client.login(
            username=self.user.username,
            password='testpass123'
        )
        sentence = Sentence.objects.create(
            english_sentence='Fourth english sentence',
            author=self.user
        )
        url = reverse('api_v1_words_in_sentences:sentence-detail', args=(sentence.pk,))
        data = {'english_sentence': '4th english sentence'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Sentence.objects.get().english_sentence, '4th english sentence')

    def test_update_sentence_not_creator(self):
        """ not the sentence's creator, can not Update (put) a sentence object. """
        # The self.client attribute will be an APIClient
        # (instead of Django's default Client) instance.
        self.client.login(
            username=self.user.username,
            password='testpass123'
        )
        sentence = Sentence.objects.create(
            english_sentence='An english sentence',
            # author=self.user
        )
        url = reverse('api_v1_words_in_sentences:sentence-detail', args=(sentence.pk,))
        data = {'english_sentence': 'One english sentence'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_sentence(self):
        """ Destroy (delete) a sentence object. """
        # The self.client attribute will be an APIClient
        # (instead of Django's default Client) instance.
        self.client.login(
            username=self.user.username,
            password='testpass123'
        )
        sentence = Sentence.objects.create(
            english_sentence='Fifth english sentence',
            author=self.user
        )
        url = reverse('api_v1_words_in_sentences:sentence-detail', args=(sentence.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_sentence_not_creator(self):
        """ not the sentence's creator, can not Destroy (delete) a sentence object. """
        # The self.client attribute will be an APIClient
        # (instead of Django's default Client) instance.
        self.client.login(
            username=self.user.username,
            password='testpass123'
        )
        sentence = Sentence.objects.create(
            english_sentence='An english sentence',
            # author=self.user
        )
        url = reverse('api_v1_words_in_sentences:sentence-detail', args=(sentence.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TagViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='Jake',
            password='testpass123'
        )
        cls.admin_user = get_user_model().objects.create_superuser(
            username='superadmin',
            password='testpass123'
        )

    def test_list_tags(self):
        """ List (get) all tags object. """
        Tag.objects.create(
            name='First tag',
        )
        url = reverse('api_v1_words_in_sentences:tag-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data[0]['name'], 'First tag')
        # with pagination:
        self.assertEqual(
            response.data['results'][0]['name'],
            'First tag'
        )

    def test_create_tag(self):
        """ Create (post) a new tag object. """
        # The self.client attribute will be an APIClient
        # (instead of Django's default Client) instance.
        self.client.login(
            username=self.user.username,
            password='testpass123'
        )
        url = reverse('api_v1_words_in_sentences:tag-list')
        data = {'name': 'Second tag'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.get().name, 'Second tag')

    def test_create_tag_not_login(self):
        """ Not login, can not Create (post) a new tag object. """
        url = reverse('api_v1_words_in_sentences:tag-list')
        data = {'name': 'A tag'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_tag(self):
        """ Retrieve (get) a tag object. """
        self.client.login(
            username=self.admin_user.username,
            password='testpass123'
        )
        tag = Tag.objects.create(
            name='Third tag',
        )
        response = self.client.get(
            reverse('api_v1_words_in_sentences:tag-detail', args=(tag.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Third tag')

    def test_retrieve_tag_not_admin_user(self):
        """ Retrieve (get) a tag object. """
        tag = Tag.objects.create(
            name='A tag',
        )
        response = self.client.get(
            reverse('api_v1_words_in_sentences:tag-detail', args=(tag.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_tag(self):
        """ Update (put) a tag object. """
        # The self.client attribute will be an APIClient
        # (instead of Django's default Client) instance.
        self.client.login(
            username=self.admin_user.username,
            password='testpass123'
        )
        tag = Tag.objects.create(
            name='Fourth tag',
        )
        url = reverse('api_v1_words_in_sentences:tag-detail', args=(tag.pk,))
        data = {'name': '4th tag'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.get().name, '4th tag')

    def test_update_tag_not_admin_user(self):
        """ not the admin_user, can not Update (put) a tag object. """
        # The self.client attribute will be an APIClient
        # (instead of Django's default Client) instance.
        self.client.login(
            username=self.user.username,
            password='testpass123'
        )
        tag = Tag.objects.create(
            name='A tag',
        )
        url = reverse('api_v1_words_in_sentences:tag-detail', args=(tag.pk,))
        data = {'name': 'One tag'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_tag(self):
        """ Destroy (delete) a tag object. """
        # The self.client attribute will be an APIClient
        # (instead of Django's default Client) instance.
        self.client.login(
            username=self.admin_user.username,
            password='testpass123'
        )
        tag = Tag.objects.create(
            name='Fifth tag',
        )
        url = reverse('api_v1_words_in_sentences:tag-detail', args=(tag.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_tag_not_admin_user(self):
        """ not the admin_user, can not Destroy (delete) a tag object. """
        # The self.client attribute will be an APIClient
        # (instead of Django's default Client) instance.
        self.client.login(
            username=self.user.username,
            password='testpass123'
        )
        tag = Tag.objects.create(
            name='An tag',
        )
        url = reverse('api_v1_words_in_sentences:tag-detail', args=(tag.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


"""
$ python manage.py test api.v1.words_in_sentences.tests.test_views --settings=a_project_config.settings.local
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.................
----------------------------------------------------------------------
Ran 17 tests in 0.734s

OK
Destroying test database for alias 'default'...
"""
