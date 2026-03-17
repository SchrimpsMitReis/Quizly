from rest_framework.viewsets import ModelViewSet
from auth_app.api.authentications import CookieJWTAuthentication
from core.utilitys.services import video_to_quiz
from quiz_app.api.permissions import QuizPermission
from quiz_app.api.serializers import QuizCreateSerializer, QuizInputSerializer
from quiz_app.models import Quiz
from rest_framework import status
# from django.http import HttpResponse
from rest_framework.response import Response
import json
from google.genai.errors import ClientError


class QuizViewSet(ModelViewSet):
    """
    ViewSet for managing quizzes.

    Supports creating quizzes from YouTube videos, listing a user's quizzes,
    retrieving quiz details, updating quiz fields, and deleting quizzes.
    """
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [QuizPermission]
    queryset = Quiz.objects.all()
    serializer_class = QuizCreateSerializer

    def create(self, request, *args, **kwargs):
        """
        the Method takes the URL from the Request, serializes it, gives it to the AI Pipe,
        serializes the result saves and respond it. All is secured 
        """
        try:
            serialized_input = self._serialize_input(request)
            quiz_as_JSON = video_to_quiz(serialized_input['url'], request)
            quiz_as_JSON['video_url'] = serialized_input['url']

            serializer = self.get_serializer(data=quiz_as_JSON)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ClientError as e:
            return Response({"detail": "Gemini quota exceeded. Please try again later."}, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request, *args, **kwargs):
        """
        Return all quizzes created by the authenticated user.
        """
        queryset = Quiz.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def _serialize_input(self, request):
        """
        Validate incoming request data containing the YouTube URL.
        """
        input_serializer = QuizInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        return input_serializer.data