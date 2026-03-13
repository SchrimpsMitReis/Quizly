


from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth_app.api.authentications import CookieJWTAuthentication
from .serializers import RegistrationSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User created successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    

class CookieTokenOptainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    # serializer_class= CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]

        user = serializer.user

        response = Response({
            "detail": "Login successfully!",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })

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

        # response.data = serializer.data
        return response
    

class CookieTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response({"detail": "Refresh token not found"}, status=status.HTTP_401_UNAUTHORIZED)

  
        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({"detail": "Refresh Token invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        
        access_token = serializer.validated_data.get("access")

        response = Response({"detail": "Token refreshed"})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="LAX"
        )
        return response



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request):


        try:
            
            self._blacklist_refresh_token(request)

            response = Response(
                {"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."},
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
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def _blacklist_refresh_token(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        refresh_token_to_delete = RefreshToken(refresh_token)
        refresh_token_to_delete.blacklist()
