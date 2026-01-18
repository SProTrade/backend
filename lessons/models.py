from django.db import models
from modules.models import modulesmodel as Modules
import uuid
class lessonsmodel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module_id = models.ForeignKey(to=Modules, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    duration = models.IntegerField(null=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    url_video = models.URLField()
    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

