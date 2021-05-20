from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from .views import UserCreateOrListView, UserOperateView
from blog.views import UserPostsView
from blog.models import Post
import time
from rest_framework.test import APIRequestFactory

class AccountsTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user. 
        self.test_user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'testpassword'
        )
        # URL for creating an account.
        self.create_url = reverse('user-create-or-list')

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
                'username': 'foobar',
                'email': 'foobar@example.com',
                'password': 'somepassword'
                }

        response = self.client.post(self.create_url , data, format='json')
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)

    def test_create_user_with_short_password(self):
        """
        Ensure user is not created for password lengths less than 8.
        """
        data = {
                'username': 'foobar',
                'email': 'foobarbaz@example.com',
                'password': 'foo'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        data = {
                'username': 'foobar',
                'email': 'foobarbaz@example.com',
                'password': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        data = {
            'username': 'foo'*60,
            'email': 'foobarbaz@example.com',
            'password': 'foobar'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        data = {
                'username': '',
                'email': 'foobarbaz@example.com',
                'password': 'foobar'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        data = {
                'username': 'testuser',
                'email': 'user@example.com',
                'password': 'testuser'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        data = {
            'username': 'testuser2',
            'email': 'test@example.com',
            'password': 'testuser'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            'username': 'foobarbaz',
            'email':  'testing',
            'passsword': 'foobarbaz'
        }


        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        data = {
                'username' : 'foobar',
                'email': '',
                'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_token_obtain_endpoint(self):
        """
        Ensure token_obtain endpoint return rigth user token
        """
        get_token_url = reverse('get-token')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user = User.objects.latest('id')
        token_from_database = Token.objects.get(user=user)
        response = self.client.post(get_token_url, data, format='json')
        token_from_response = response.data['token']
        self.assertEqual(token_from_database.key, token_from_response)

    def test_posts_ordering_from_creation_date(self):
        """
        Ensure the user posts ordering from creation date
        """
        need_posts = 15
        post_counter = 0
        
        # create 3 posts to testuser 
        for i in range(1, need_posts, 1):
            post_title = 'Post# %s' % (i)
            Post.objects.create(
                owner=self.test_user,
                title=post_title,
                text='test_text'
            )
            time.sleep(0.05)
            post_counter = i
        
        view = UserPostsView.as_view()
        factory = APIRequestFactory()
        user_id = self.test_user.id
        request = factory.get('/api/users/%s/posts' % (user_id))
        response = view(request, pk=user_id)
        result = response.render()
        # check if last created post on top of response data
        last_post = Post.objects.all().order_by('-created_at')[0]
        self.assertEqual(result.data[0]['id'], last_post.id)
    


    def test_users_sorting_from_max_posts(self):
        """
        Check users sorting from max posts.
        If its work rigth the user which have maximum posts\
        must be first in the response.data
        """
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
        view = UserCreateOrListView.as_view()
        factory = APIRequestFactory()
        request_max = factory.get('/api/users?sorting=from_max')
        response_with_max_sorting = view(request_max)
        result_max = response_with_max_sorting.render()
        # check if max_posts_user on top of response data
        self.assertEqual(result_max.data[0]['username'], max_posts_user.username)

    def test_users_sorting_from_min_posts(self):
        """
        Check users sorting from min posts.
        If its work rigth the user which have minimum posts\
        must be first in the response.data
        """
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
        view = UserCreateOrListView.as_view()
        factory = APIRequestFactory()
        request_min = factory.get('/api/users?sorting=from_min')
        response_with_min_sorting = view(request_min, sorting='from_min')
        result_min = response_with_min_sorting.render()
        # check if min_posts_user on top of response data
        self.assertEqual(result_min.data[0]['username'], min_posts_user.username)