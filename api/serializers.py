from rest_framework import serializers
from courses.models import coursesmodel as Courses
from modules.models import modulesmodel as Modules
from lessons.models import lessonsmodel as Lessons
from exercises.models import exercisesmodel as Exercises

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
       
        fields = ['title', 'duration', 'lessons_quantity']

class ModulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modules
       
        fields = ['title', 'duration', 'lessons_quantity']        

class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
       
        fields = ['title', 'duration', 'url_video']        

class ExercisesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
       
        fields = ['title', 'duration']       