from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz
from .serializers import QuizSerializer

class HealthCheckView(APIView):
    """Проверка работы API"""
    def get(self, request):
        return Response({
            "status": "ok",
            "message": "API работает",
            "timestamp": "2024-01-01T00:00:00Z"
        })

class QuizListView(APIView):
    """Получить все квизы"""
    def get(self, request):
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response({
            "success": True,
            "count": len(serializer.data),
            "quizzes": serializer.data
        })

class QuizDetailView(APIView):
    """Получить конкретный квиз"""
    def get(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            serializer = QuizSerializer(quiz)
            return Response({
                "success": True,
                "quiz": serializer.data
            })
        except Quiz.DoesNotExist:
            return Response({
                "success": False,
                "error": "Quiz not found"
            }, status=status.HTTP_404_NOT_FOUND)