from django.db import models
from modules.models import modulesmodel as Modules
import uuid
class exercisesmodel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module_id = models.ForeignKey(to=Modules, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    duration = models.IntegerField(null=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тести'


class Question(models.Model):
    exercise = models.ForeignKey(
        'exercisesmodel', 
        related_name='questions', 
        on_delete=models.CASCADE
    )
    question_text = models.TextField(verbose_name="Текст питання")
    
    def __str__(self):
        return self.question_text[:50]

    class Meta:
        verbose_name = 'Питання'
        verbose_name_plural = 'Питання'

class Choice(models.Model):
    question = models.ForeignKey(
        Question, 
        related_name='choices', 
        on_delete=models.CASCADE
    )
    choice_text = models.CharField(max_length=255, verbose_name="Варіант відповіді")
    is_correct = models.BooleanField(default=False, verbose_name="Це правильна відповідь?")

    def __str__(self):
        return self.choice_text