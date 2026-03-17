from django.urls import path
from auth_app.api.views import LoginView, CookieTokenRefreshView, LogoutView, RegistrationView


urlpatterns = [
    # Endpoint for creating a new user account
    path('register/', RegistrationView.as_view(), name='registration'),

    # Endpoint for user login, returns JWT access and refresh tokens
    path('login/', LoginView.as_view(), name='token_obtain_pair'),

    # Endpoint for refreshing the access token using a refresh token
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),

    # Endpoint for logging out and invalidating tokens
    path('logout/', LogoutView.as_view(), name='logout'),
]