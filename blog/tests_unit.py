from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import Post
import time
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

   

"""
def test_users_sorting_from_max_posts(self):
        ""
        Check users sorting from max posts.
        If its work rigth the user which have maximum posts\
        must be first in the response.data
        ""
        # create user which have a 3 posts
        max_posts_user = self.test_user

        # create 3 posts to max_posts_user
        for iter in range(1,4,1):
            post_title = "Post# %s" % (iter)
            Post.objects.create(
                owner=max_posts_user,
                title=post_title,
                text='test_text'
            )

        # create user which have a 2 posts
        middle_posts_user = User.objects.create_user(
            'middle_posts_user',
            'test2@example.com',
            'testpassword2'
        )

        # create 2 posts to middle_posts_user
        for iter in range(1,3,1):
            post_title = "Post# %s" % (iter)
            Post.objects.create(
                owner=middle_posts_user,
                title=post_title,
                text='test_text'
            )

        # create user which have a 1 post
        min_posts_user = User.objects.create_user(
            'min_posts_user',
            'test3@example.com',
            'testpassword3'
        )

        # create 1 post to min_posts_user
        for iter in range(1,2,1):
            post_title = "Post# %s" % (iter)
            Post.objects.create(
                owner=min_posts_user,
                title=post_title,
                text='test_text'
            )

        # request to page all users with ordering from max posts
        view = UserList.as_view()
        factory = APIRequestFactory()
        request_max = factory.get('/api/user/all/from_max')
        response_with_max_sorting = view(request_max, sorting='from_max')
        result_max = response_with_max_sorting.render()
        # check if max_posts_user on top of response data
        self.assertEqual(result_max.data[0]['username'], max_posts_user.username)
    
    def test_users_sorting_from_min_posts(self):
        ""
        Check users sorting from min posts.
        If its work rigth the user which have minimum posts\
        must be first in the response.data
        ""
        # create user which have a 3 posts
        max_posts_user = self.test_user

        # create 3 posts to max_posts_user
        for iter in range(1,4,1):
            post_title = "Post# %s" % (iter)
            Post.objects.create(
                owner=max_posts_user,
                title=post_title,
                text='test_text'
            )

        # create user which have a 2 posts
        middle_posts_user = User.objects.create_user(
            'middle_posts_user',
            'test2@example.com',
            'testpassword2'
        )

        # create 2 posts to middle_posts_user
        for iter in range(1,3,1):
            post_title = "Post# %s" % (iter)
            Post.objects.create(
                owner=middle_posts_user,
                title=post_title,
                text='test_text'
            )

        # create user which have a 1 post
        min_posts_user = User.objects.create_user(
            'min_posts_user',
            'test3@example.com',
            'testpassword3'
        )
        
        # create 1 post to min_posts_user
        for iter in range(1,2,1):
            post_title = "Post# %s" % (iter)
            Post.objects.create(
                owner=min_posts_user,
                title=post_title,
                text='test_text'
            )

        # request to page all users with ordering from min posts
        view = UserList.as_view()
        factory = APIRequestFactory()
        request_min = factory.get('/api/user/all/from_min')
        response_with_min_sorting = view(request_min, sorting='from_min')
        result_min = response_with_min_sorting.render()
        # check if min_posts_user on top of response data
        self.assertEqual(result_min.data[0]['username'], min_posts_user.username)
"""