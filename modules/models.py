from django.db import models
from courses.models import coursesmodel as Courses
import uuid
class modulesmodel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_id = models.ForeignKey(to=Courses, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    duration = models.IntegerField(null=False)
    lessons_quantity = models.IntegerField(null=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модулі'

