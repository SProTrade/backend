from django.contrib import admin
from .models import coursesmodel

@admin.register(coursesmodel)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'lessons_quantity', 'exercises_quantity', 'is_published', 'created_at')
    search_fields = ('title', 'created_at')
    list_filter = ('is_published', 'created_at')

    class Meta:
        model = coursesmodel
        verbose_name = 'Курс'
        verbose_name_plural = 'Курси'
# Register your models here.
