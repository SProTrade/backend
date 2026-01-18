from django.contrib import admin
from .models import modulesmodel

@admin.register(modulesmodel)
class ModulesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'lessons_quantity', 'is_published', 'created_at')
    search_fields = ('title', 'created_at')
    list_filter = ('is_published', 'created_at')

    class Meta:
        model = modulesmodel
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модулі'
# Register your models here.z
