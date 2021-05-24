from itertools import chain

from django.contrib.auth import get_user_model
from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from .models import Post, Subscribe, ReadedPostsList
from .paginators import UserPostsResultsPagination

import operator

class PostCreate(generics.CreateAPIView):
    """
    Post creation\n
    """
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Create new post\n
            - only for authenticated users\n
            EXAMPLE: curl  -H 'Content-Type: application/json'\n
                --data '{"title":"My first post","text":"Very small text"}'\n
                http://127.0.0.1:8000/api/blog/ - create new post\n 
        """
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class FeedView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    Dynamically generate post feed
    """
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserPostsResultsPagination

    def get_queryset(self, *args, **kwargs):
        qs = Post.objects.none()
        user_subscriptions = self.request.user.get_subs_list()
        if user_subscriptions is not None:
            for subs in user_subscriptions.subscribed_to.all():
                to_user = subs.to
                created = subs.subscribed_time
                subs_posts = to_user.get_posts_from_date(created)
                qs = list(chain(qs, subs_posts))
            qs = self._filter_qs(self.request, qs)
            return self._sorted(qs)
        return qs
            
    def _sorted(self, data, sorting='from_max'):
        return sorted(data, key=operator.attrgetter('created_at'), reverse=True)

    def get(self, request, *args, **kwargs):
        """
        Return all your posts in feed\n
            - only for authenticated users\n
            - have optional parameter "filter" = "readed" or "unreaded(default)"\n
            EXAMPLE: curl http://127.0.0.1:8000/api/blog/feed?filter=unreaded - return all unreaded posts in your feed
            EXAMPLE: curl http://127.0.0.1:8000/api/blog/feed?filter=readed - return all readed posts in your feed
            - results paginate by 10 items per page
        """
        return self.list(request, *args, **kwargs)
    
    def _filter_qs(self, request, queryset):
        filtering = request.GET.get('filter', 'unreaded')
        r_list = ReadedPostsList.objects.get(owner=request.user)
        filtered_unreaded_qs = Post.objects.none()
        filtered_readed_qs = Post.objects.none()
        readed_posts = r_list.were_read.all()
        for item in queryset:
            # any best solution for create qs_item?
            # because it must be iterated
            qs_item = Post.objects.filter(id=item.id)
            try:
                res = readed_posts.get(post=item)
                filtered_readed_qs = list(chain(filtered_readed_qs, qs_item))
            except:
                
                filtered_unreaded_qs = list(chain(filtered_unreaded_qs, qs_item))
        if filtering == 'unreaded':
            return filtered_unreaded_qs
        if filtering == 'readed':
            return filtered_readed_qs
     


class UserPostsView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    All posts of user \n
    """
    serializer_class = serializers.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        try:
            from_user = get_user_model().objects.get(id=self.kwargs['pk'])
            if from_user is not None:
                qs = Post.objects.filter(owner=from_user)
                return qs
        except:
            return Post.objects.none()
        
    def get(self, request, *args, **kwargs):
        """
        Return all posts of user\n
            - Allow any user\n
            EXAMPLE: curl http://127.0.0.1:8000/api/blog/12/posts/ - return all user posts which id=12\n
                posts ordered by creation time 
        """
        return self.list(request, *args, **kwargs)


class SubscribeCreateOrListView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    Create subscribe on user or get your subscribes list
    """
    serializer_class = serializers.SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscribe.objects.filter(subscribeslist__owner = self.request.user)

    def get(self, request, *args, **kwargs):
        """
        Return all your subscribes\n
            - only for authenticated users\n
            EXAMPLE: curl http://127.0.0.1:8000/api/blog/subscribes/ - return all your subscribes\n 
        """
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """
        Subscribe you on user\n
            - only for authenticated users\n
            EXAMPLE: curl --data "to=14" http://127.0.0.1:8000/api/blog/subscribes/ - subscribe you on user which id=14\n 
        """
        return self.create(request, *args, **kwargs)
        

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            request_user_subs_list = request.user.get_subs_list()
            subscribed = False
            try:
                if request_user_subs_list.subscribed_to.all().get(to_id=request.data.get('to')):
                    print(request_user_subs_list.subscribed_to.all().get(to=request.data.get('to')))
                    subscribed = True
                    return Response({'detail' : 'You already subscribe to this user'}, status=status.HTTP_200_OK)
            except:
                if not subscribed:
                    subscribe = serializer.save()
                    request_user_subs_list.subscribed_to.add(subscribe)
                    request_user_subs_list.save()
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) 

class SubscribeOperateView(generics.GenericAPIView, mixins.DestroyModelMixin):
    """
    Deletion of subscribe
    """
    serializer_class = serializers.SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscribe.objects.filter(subscribeslist__owner = self.request.user)

    def delete(self, request, *args, **kwargs):
        """
        Unsubscribe on user\n
            - only for authenticated users\n
            EXAMPLE: curl -X DELETE http://127.0.0.1:8000/api/blog/subscribes/2/ - delete your subscribe which id=2
        """
        return self.destroy(request, *args, **kwargs)


class ReadedPostsView(generics.GenericAPIView, mixins.CreateModelMixin):
    """
    Mark post as readed
    """
    serializer_class = serializers.ReadedPostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Mark post as readed\n
            - only for authenticated users\n
            EXAMPLE: curl  -H 'Content-Type: application/json'\n
            --data '{"post":"14"}' http://127.0.0.1:8000/api/blog/readed/ - mark post which id=14 as readed\n 
        """
        already = request.user.check_in_readed_posts(request.data)
        #print(already)
        if not already:
            in_feed = request.user.check_in_feed(request.data)
            #print(in_feed)
            if in_feed:
                return self.create(request, *args, **kwargs)
            return Response({'detail':'This post is not in feed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Already marked "as read"'}, status=status.HTTP_200_OK)

    
    def perform_create(self, serializer):
        readed_post = serializer.save()
        r_list = ReadedPostsList.objects.get(owner=self.request.user)
        r_list.were_read.add(readed_post)