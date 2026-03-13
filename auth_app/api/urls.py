


from django.urls import path
from auth_app.api.views import CookieTokenOptainPairView, CookieTokenRefreshView, LogoutView, RegistrationView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', CookieTokenOptainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='token_obtain_pair'),
]
