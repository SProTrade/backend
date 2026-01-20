from rest_framework import serializers
from courses.models import coursesmodel as Courses
from modules.models import modulesmodel as Modules
from lessons.models import lessonsmodel as Lessons
from exercises.models import exercisesmodel, Question, Choice

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
       
        fields = ['title', 'description', 'duration', 'lessons_quantity', 'exercises_quantity']

class ModulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modules
       
        fields = ['id', 'title', 'duration', 'lessons_quantity']        

class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
       
        fields = ['id', 'title', 'duration', 'url_video']        



class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'is_correct']
    
    def to_representation(self, instance):
        # Отримуємо стандартний словник даних
        ret = super().to_representation(instance)
        
        # Якщо is_correct дорівнює False, видаляємо це поле з JSON
        if not ret.get('is_correct'):
            ret.pop('is_correct')
            
        return ret
class QuestionSerializer(serializers.ModelSerializer):

    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'choices']

class ExercisesSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = exercisesmodel
        fields = ['id', 'title', 'questions']