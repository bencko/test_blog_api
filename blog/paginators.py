from rest_framework.pagination import PageNumberPagination


class UserPostsResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'user_posts_page_size'
