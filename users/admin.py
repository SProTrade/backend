from django.contrib import admin
from .models import Users

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'pocket_id', 'is_registered', 'balance', 'progress', 'current_lesson', 'click_id', 'created_at')
    search_fields = ('telegram_id', 'pocket_id')
    list_filter = ('is_registered', 'created_at')

    class Meta:
        model = Users
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'