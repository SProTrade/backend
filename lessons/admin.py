from django.contrib import admin
from .models import lessonsmodel

@admin.register(lessonsmodel)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'created_at', 'url_video', 'getTitle')
    search_fields = ('title', 'created_at')
    list_filter = ('is_published', 'created_at')
    @admin.display(description="module", ordering="module_id__title")
    def getTitle(self, obj):
        return obj.module_id.title if obj.module_id else "-"
    class Meta:
        model = lessonsmodel
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
# Register your models here.z
