from django.db import models


class Quiz(models.Model):
    """Минимальная модель квиза"""
    objects = None
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.title


class Question(models.Model) :
    """Минимальная модель вопроса"""
    objects = None
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self) :
        return f"{self.quiz.title} - {self.text[:50]}"


class Answer(models.Model) :
    """Минимальная модель ответа"""
    objects = None
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self) :
        return self.text