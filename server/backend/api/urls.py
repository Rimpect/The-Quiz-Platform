from django.urls import path
from .views import HealthCheckView, QuizListView, QuizDetailView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('quizzes/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz-detail'),
]