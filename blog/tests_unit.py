from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import Post

from rest_framework.test import APIRequestFactory


class BlogTest(APITestCase):
    def setUp(self):
        # Create test_user instance directly from the User model manager. 
        self.test_user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'testpassword'
        )

        # URL for creating a post.
        self.create_url = reverse('post-create')

    def test_create_post_from_not_auth_user(self):
        data = {
                'title': 'test title',
                'text': 'test_text'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_from_auth_user(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
                'title': 'test title',
                'text': 'test_text'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_with_no_title(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
                'title': '',
                'text': 'test_text'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_post_with_no_body_text(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
                'title': 'test title',
                'text': ''
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_post_check_owner(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
                'title': 'test title',
                'text': 'test_text'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.data['owner'], self.test_user.id)

   

