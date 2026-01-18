from django.contrib import admin
from .models import exercisesmodel

@admin.register(exercisesmodel)
class ExercisesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'created_at', 'getTitle')
    search_fields = ('title', 'created_at')
    list_filter = ('is_published', 'created_at')
    @admin.display(description="module", ordering="module_id__title")
    def getTitle(self, obj):
        return obj.module_id.title if obj.module_id else "-"
    class Meta:
        model = exercisesmodel
        verbose_name = 'Тест'
        verbose_name_plural = 'Тести'