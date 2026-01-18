from django.db import models
import uuid
class coursesmodel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=150)
    duration = models.IntegerField(null=False)
    lessons_quantity = models.IntegerField(null=False)
    exercises_quantity = models.IntegerField(null=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курси'
# Create your models here.
