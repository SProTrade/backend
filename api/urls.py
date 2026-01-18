from django.urls import path, include
from . import views

urlpatterns = [
    path('user/', views.get_user_info, name='get_user_info'),
    path('user/create/', views.create_user, name='create_user'),
    path('user/poid/', views.update_user_pocketid, name='update_user_pocket_id'),
    path('user/balance/', views.update_user_balance, name='update_user_balance'),
    path('courses/all/', views.get_courses_info, name='get_courses_info'),
    path('modules/course/<uuid:course_id>/', views.get_modules_info, name='get_modules_info'),
    path('lessons/module/<uuid:module_id>/', views.get_lessons_info, name='get_lessons_info'),
    path('exercises/module/<uuid:module_id>/', views.get_exercises_info, name='get_exercises_info')
]