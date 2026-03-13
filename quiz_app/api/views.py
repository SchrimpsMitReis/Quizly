from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auth_app.api.authentications import CookieJWTAuthentication
from core.utilitys.services import video_to_quiz
from quiz_app.api.permissions import QuizPermission
from quiz_app.api.serializers import QuizCreateSerializer, QuizInputSerializer
from quiz_app.models import Quiz
from rest_framework import status


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
        Create a new quiz from a provided YouTube URL.
        The video is processed and converted into quiz questions.
        """
        serialized_input = self._serialize_input(request)
        quiz_as_JSON = video_to_quiz(serialized_input['url'], request)
        user = request.user.id
        quiz_as_JSON['video_url'] = serialized_input['url']

        serializer = self.get_serializer(data=quiz_as_JSON)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """
        Return all quizzes created by the authenticated user.
        """
        self.queryset = Quiz.objects.filter(user=request.user)
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single quiz by its ID.
        """
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update quiz fields such as title or description.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a quiz and its related questions.
        """
        return super().destroy(request, *args, **kwargs)

    def _serialize_input(self, request):
        """
        Validate incoming request data containing the YouTube URL.
        """
        input_serializer = QuizInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        return input_serializer.data