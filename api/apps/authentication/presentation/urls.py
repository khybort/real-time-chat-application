from django.urls import path
from apps.authentication.presentation.auth_view import RegisterView, LoginView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
