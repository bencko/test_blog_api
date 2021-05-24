import time

from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory

from .views import UserPostsView
from .models import Post, Subscribe


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

    def test_subscribe_and_feed_view(self):
        """
        Test subscribe and feed generation
        """
        subscribe_to_user = User.objects.create_user(
            'subscribe_to_user',
            'test2@example.com',
            'testpassword'
        )
        subscribe_url = reverse('subscribe-create-or-list')

        self.client.login(username='testuser', password='testpassword')
        data = {
                'to': subscribe_to_user.id,
        }
        response = self.client.post(subscribe_url, data, format='json')
        # check id user who we subscribe
        self.assertEqual(response.data['to'], subscribe_to_user.id)
        my_susbscribe_id_from_response = response.data['id']
        my_susbscribe_from_db = Subscribe.objects.get(to=subscribe_to_user.id)
        # check id of subscribe - its same in db and in response?
        self.assertEqual(
            my_susbscribe_id_from_response,
            my_susbscribe_from_db.id
        )

        post_needed = 6

        # create 5 posts to subscribe_to_user
        for i in range(1, post_needed, 1):
            post_title = 'Post# %s' % (i)
            Post.objects.create(
                owner=subscribe_to_user,
                title=post_title,
                text='test_text'
            )
            time.sleep(0.05)

        response = self.client.get('/api/blog/feed/')
        # check we have a needed count of new posts in feed
        self.assertEqual(response.data['count'], post_needed - 1)

    def test_subscribe_create_and_delete(self):
        """
        Test creation and deletion subsccribe
        """
        subscribe_to_user = User.objects.create_user(
            'subscribe_to_user',
            'test2@example.com',
            'testpassword'
        )
        subscribe_url = reverse('subscribe-create-or-list')

        self.client.login(username='testuser', password='testpassword')
        data = {
                'to': subscribe_to_user.id,
        }
        # we subscribe to subscribe_to_user
        crate_response = self.client.post(subscribe_url, data, format='json')
        # check if subscribe is added
        sub = Subscribe.objects.get(to=subscribe_to_user.id)
        self.assertEqual(sub.to.id, subscribe_to_user.id)

        delete_response = self.client.delete(
            id=sub.id,
            path='/api/blog/subscribes/%s/' % sub.id
        )
        self.assertEqual(
            delete_response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_mark_as_readed_in_feed(self):
        subscribe_to_user = User.objects.create_user(
            'subscribe_to_user',
            'test2@example.com',
            'testpassword'
        )
        subscribe_url = reverse('subscribe-create-or-list')

        self.client.login(username='testuser', password='testpassword')
        data = {
                'to': subscribe_to_user.id,
        }
        response = self.client.post(subscribe_url, data, format='json')
        # check id user who we subscribe
        self.assertEqual(response.data['to'], subscribe_to_user.id)
        my_susbscribe_id_from_response = response.data['id']
        my_susbscribe_from_db = Subscribe.objects.get(to=subscribe_to_user.id)
        # check id of subscribe - its same in db and in response?
        self.assertEqual(
            my_susbscribe_id_from_response,
            my_susbscribe_from_db.id
        )

        post_needed = 6

        # create 5 posts to subscribe_to_user
        for i in range(1, post_needed, 1):
            post_title = 'Post# %s' % (i)
            Post.objects.create(
                owner=subscribe_to_user,
                title=post_title,
                text='test_text'
            )
            time.sleep(0.05)

        response = self.client.get('/api/blog/feed/')
        # check we have a needed count of new posts in feed
        self.assertEqual(response.data['count'], post_needed - 1)
        data_to_mark = {
            'post': response.data['results'][0]['id']
        }
        mark_url = reverse('mark-as-readed')
        marked_response = self.client.post(
            mark_url, data_to_mark,
            format='json'
        )
        self.assertEqual(marked_response.status_code, status.HTTP_201_CREATED)
        response_after_mark = self.client.get('/api/blog/feed/')
        # minus 1 deleted post
        self.assertEqual(
            response_after_mark.data['count'],
            post_needed - (1+1)
        )
