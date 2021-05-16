from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import Post
from .views import UserPostList
import time
from rest_framework.test import APIRequestFactory


class BlogTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user. 
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
        
        view = UserPostList.as_view()
        factory = APIRequestFactory()
        user_id = self.test_user.id
        request = factory.get('/api/post/from_user/%s' % (user_id))
        response = view(request, pk=user_id)
        result = response.render()
        # check if last created post on top of response data
        last_post = Post.objects.all().order_by('-created_at')[0]
        self.assertEqual(result.data[0]['id'], last_post.id)
        