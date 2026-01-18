from django.contrib import admin
from .models import exercisesmodel, Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4  
    min_num = 2 

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('question_text',) 

@admin.register(exercisesmodel)
class ExercisesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'created_at', 'getTitle')
    search_fields = ('title', 'created_at')
    list_filter = ('is_published', 'created_at')
    inlines = [QuestionInline] 

    @admin.display(description="module", ordering="module_id__title")
    def getTitle(self, obj):
        return obj.module_id.title if obj.module_id else "-"

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'exercise')
    list_filter = ('exercise',)
    inlines = [ChoiceInline] 