from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status


class IntegrityTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        # URL for creating a post.
        self.create_user_url = reverse('user-create-or-list')
        self.create_post_url = reverse('post-create')

    def test_register_user_and_create_post(self):
        user_data = {
                'username': 'testuser',
                'email': 'testemail@test.com',
                'password': 'StrongPass2021'
        }
        register_user = self.client.post(
            self.create_user_url,
            user_data,
            format='json'
        )

        self.assertEqual(register_user.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=user_data['username'])
        self.client.force_authenticate(user)
        post_data = {
                'title': 'test title',
                'text': 'test_text'
        }
        created_post = self.client.post(
            self.create_post_url,
            post_data,
            format='json'
        )
        self.assertEqual(created_post.status_code, status.HTTP_201_CREATED)
