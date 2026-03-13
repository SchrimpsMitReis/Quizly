from django.http import HttpResponse
import json
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from auth_app.api.authentications import CookieJWTAuthentication
from .serializers import RegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class RegistrationView(APIView):
    """
    API endpoint for registering a new user.
    Accessible without authentication.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Create a new user account using the RegistrationSerializer.
        """
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return HttpResponse(
            json.dumps({"detail": "User created successfully!"}),
            content_type="application/json",
            status=status.HTTP_201_CREATED
            )
        

class CookieTokenOptainPairView(TokenObtainPairView):
    """
    Custom login view that authenticates a user and stores
    the access and refresh tokens in HttpOnly cookies.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Validate login credentials and return authentication cookies.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]

        user = serializer.user

        response = HttpResponse(
            json.dumps({
                "detail": "Login successfully!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }),
            content_type="application/json",
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=True,
            samesite="LAX"
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="LAX"
        )

        return response
    

class CookieTokenRefreshView(TokenRefreshView):
    """
    Refresh the access token using the refresh token stored in cookies.
    """

    def post(self, request, *args, **kwargs):
        """
        Generate a new access token if the refresh token is valid.
        """
        
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return HttpResponse(
                json.dumps(
                    {"detail": "Refresh token not found"}),
                    content_type="application/json", 
                    status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return HttpResponse(
                json.dumps({"detail": "Refresh Token invalid"}), 
                content_type="application/json",
                status=status.HTTP_401_UNAUTHORIZED)
        

        access_token = serializer.validated_data.get("access")

        response = HttpResponse(
            json.dumps({"detail": "Token refreshed"}), 
            content_type="application/json", 
            status=status.HTTP_200_OK)
        
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="LAX"
        )
        return response



class LogoutView(APIView):
    """
    Logout endpoint that deletes authentication cookies
    and blacklists the refresh token.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request):
        """
        Invalidate the refresh token and remove authentication cookies.
        """

        try:
            
            self._blacklist_refresh_token(request)

            response = HttpResponse(
                json.dumps({"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."}),
                content_type="application/json",
                status=status.HTTP_200_OK
            )

            response.delete_cookie(
                key="access_token",
                path="/")
            response.delete_cookie(
                key="refresh_token",
                path="/"
                )

            return response
        
        except Exception:
            return HttpResponse(
                json.dumps({"error": "Invalid token"}),
                content_type="application/json",
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def _blacklist_refresh_token(self, request):
        """
        Add the refresh token to the blacklist so it can no longer be used.
        """
        refresh_token = request.COOKIES.get("refresh_token")
        refresh_token_to_delete = RefreshToken(refresh_token)
        refresh_token_to_delete.blacklist()