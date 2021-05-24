from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('openapi', get_schema_view(
        title="WB-TECH TEST",
        description="Documentation for API endpoints",
        version="1.0.0"
    ), name='openapi-schema'),
    path('admin/', admin.site.urls),
    path('api/users/', include('accounts.urls')),
    path('api/blog/', include('blog.urls')),
    path('api-docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
