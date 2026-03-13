from rest_framework.serializers import ModelSerializer, Serializer, URLField
from quiz_app.models import Quiz, Question

class QuizInputSerializer(Serializer):
    """
    Serializer used to receive a YouTube URL for quiz generation.
    """
    url = URLField()


class QuestionsNestedSerializer(ModelSerializer):
    """
    Serializer for representing quiz questions inside a quiz.
    Used as a nested serializer within QuizCreateSerializer.
    """
    
    class Meta:
        model = Question
        fields = [
            'id',
            'question_title',
            'question_options',
            'answer',
            'created_at',
            'updated_at'
        ]


class QuizCreateSerializer(ModelSerializer):
    """
    Serializer for creating a quiz together with its nested questions.
    """

    questions = QuestionsNestedSerializer(many=True)

    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'updated_at',
            'video_url',
            'questions'            
        ]

    def create(self, validated_data):
        """
        Create a Quiz instance and its related Question objects.
        """
        questions_data = validated_data.pop("questions")
        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            Question.objects.create(quiz=quiz, **question_data)

        return quiz