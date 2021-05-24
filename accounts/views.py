
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics, views
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.authtoken import views as auth_views
from rest_framework.authtoken.models import Token
from rest_framework import status
 
from . import serializers


class ObtainAuthToken(auth_views.ObtainAuthToken):
    """
    Send to this endpoint username and password\
    and it return token for this account\n
        EXAMPLE: curl  -H 'Content-Type: application/json'\n
                --data '{"username":"bobby123":"StrongPass2021"}'\n
                http://127.0.0.1:8000/api/users/api-token-auth/ - return you token for auth
    """

    def get_serializer_class(self):
        return AuthTokenSerializer


class UserCreateOrListView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    Creation and list user
    """
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        qs = get_user_model().objects.all()
        return qs

    def post(self, request, *args, **kwargs):
        """
        Create new user\n
            - Allow any user\n
            EXAMPLE: curl  -H 'Content-Type: application/json'\n
                --data '{"username":"michael007","email":"my_email@ex.com", "password":"StrongPass2021"}'\n
                http://127.0.0.1:8000/api/users/ - creae new user\n 
            - need unique username and email
        """
        return self.create(request)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            user = serializer.save()
            if user:
                token = Token.objects.get(user=user)
                json = serializer.data
                json['token'] = token.key
                headers = self.get_success_headers(serializer.data)
                return Response(json, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request,  *args, **kwargs):
        """
        Return all users list\n
            - Allow any user\n
            - have optional parameter "sorting" = "from_max(default)" or "from_min"\n
            EXAMPLE: curl http://127.0.0.1:8000/api/users?sorting=from_max - return all users ordered by total posts count from max
            EXAMPLE: curl http://127.0.0.1:8000/api/users?sorting=from_min - return all users ordered by total posts count from min
        """
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        sorting = request.GET.get('sorting', 'from_max')
        serializer = self.get_serializer(queryset, many=True)
        data = self._sorted_serializer_data(serializer.data, sorting)
        return Response(data)
    
    # method for sorting serialized data
    def _sorted_serializer_data(self, data, sorting='from_max'):
        if sorting == 'from_max':
            return sorted(data, key=lambda k: k['total_posts'], reverse=True)
        return sorted(data, key=lambda k: k['total_posts'])


class UserOperateView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()

    def get(self, request, *args, **kwargs):
        """
        User detail\n
            - Allow any user\n
            EXAMPLE: curl http://127.0.0.1:8000/api/users/4 - return user info which id=4
        """
        return self.retrieve(request, *args, **kwargs)









            