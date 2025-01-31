from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

admin.site.site_header = "Real Time Chat Application Admin"
admin.site.site_title = "Real Time Chat Application Admin Portal"
admin.site.index_title = "Welcome to the Real Time Chat Application Portal"


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="API endpoints for the Real Time Chat Application project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/auth/', include('apps.authentication.presentation.urls')),
    path('api/chat/', include('apps.chat.presentation.urls')),
    
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
