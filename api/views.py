from django.shortcuts import render, HttpResponse
from users.models import Users
from courses.models import coursesmodel as Courses 
from modules.models import modulesmodel as Modules
from lessons.models import lessonsmodel as Lessons
from exercises.models import exercisesmodel as Exercises
from exercises.models import Question, Choice
import json
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED, HTTP_409_CONFLICT
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from decimal import Decimal as dou
from .tokens import generate_tokens
from .serializers import CoursesSerializer, ModulesSerializer, LessonsSerializer, ExercisesSerializer
from rest_framework.permissions import AllowAny
from tradebot.logic import get_data

#__________------------ Views for TOKENS ------------__________#

@api_view(['POST'])
@permission_classes([]) 
def custom_login(request):
    telegram_id = request.data.get('telegram_id')
   
    user = Users.objects.filter(telegram_id=telegram_id).first()
    
    if user:
        access_token, refresh_token = generate_tokens(user = user)
        return Response({'access_token': access_token, 'refresh_token': refresh_token})
    return Response({'error': 'Invalid user'}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny]) 
def refresh_token(request):
    refresh_token = request.data.get('refresh_token')
    if not refresh_token:
        return Response({'error': 'Refresh token is required'}, status=400)
    try:
        access_token, new_refresh_token = generate_tokens(refresh_token=refresh_token)
        return Response({'access_token': access_token, 'refresh_token': new_refresh_token})
    except ValueError as e:
        return Response({'error': str(e)}, status=400)


#__________------------ Views for USERS ------------__________#



@api_view(['GET'])
def get_user_info(request):
    if request.method != 'GET':
        return Response(data = {"message": "Method not allowed"}, status=HTTP_405_METHOD_NOT_ALLOWED)

    if request.headers.get('Authorization') is None or request.headers.get('Authorization') == "":
        return Response(data = {"message": "Authorization header is missing."}, status=HTTP_401_UNAUTHORIZED)

    try:
        user = request.user 
        return Response(data={"message": "User found.", "user": ({
        'id' : user.id,
        'telegram_id': user.telegram_id,
        'pocket_id': user.pocket_id,
        'is_registered': user.is_registered,
        'balance': user.balance,
        'click_id': user.click_id
        })})
    
    except Users.DoesNotExist:
        return Response(data = {"message": "User not found."}, status=HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([])
def create_user(request):
    if request.method != 'POST':
        return Response(data = {"message": "Method not allowed"}, status=HTTP_405_METHOD_NOT_ALLOWED)
    
    params = request.POST
    telegram_id = params.get('telegram_id')
    
    if not telegram_id:
        return Response(data = {"message": "telegram_id is required."}, status=HTTP_400_BAD_REQUEST)
    
    user = Users.objects.filter(telegram_id=telegram_id).first()
    if user:
        return Response(data = {"message": "User already exists.", "user": ({
        'id' : user.id,
        'telegram_id': user.telegram_id,
        'pocket_id': user.pocket_id,
        'is_registered': user.is_registered,
        'balance': user.balance,
        'click_id': user.click_id
        })}, status=HTTP_409_CONFLICT)
    
    user = Users.objects.create(telegram_id=telegram_id)
    user.save()
    user.generate_click_id()
    
    return Response(data={"message": "User created.", "user": ({
        'id' : user.id,
        'telegram_id': int(user.telegram_id),
        'pocket_id': user.pocket_id,
        'is_registered': user.is_registered,
        'balance': user.balance,
        'click_id': user.click_id,
        'click_id': user.click_id
        })}, status=HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([])
def update_user_pocketid(request):
    if request.method != 'POST':
        return Response(data = {"message": "Method not allowed"}, status=HTTP_405_METHOD_NOT_ALLOWED)
    
    params = request.query_params
    print(params)
    click_id = params.get('click_id')
    pocket_id = params.get('pocket_id')

    if not click_id or not pocket_id:
        return Response(data = {"message": "click_id and pocket_id are required."}, status=HTTP_400_BAD_REQUEST)
    
    try:
        user = Users.objects.get(click_id=click_id)
        user.pocket_id = pocket_id
        user.is_registered = True
        user.save()
        return Response(data={"message": "Pocket Option ID updated.", "user": ({
        'id' : user.id,
        'telegram_id': user.telegram_id,
        'pocket_id': user.pocket_id,
        'is_registered': user.is_registered,
        'balance': user.balance,
        'click_id': user.click_id
        })}, status=HTTP_200_OK)
    
    except Users.DoesNotExist:
        return Response(data = {"message": "User not found."}, status=HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
@permission_classes([])
def update_user_balance(request):
    if request.method != 'POST':
        return Response(data = {"message": "Method not allowed"}, status=HTTP_405_METHOD_NOT_ALLOWED)
    
    params = request.query_params
    pocket_id = params.get('pocket_id')
    balance = params.get('balance')

    if not pocket_id or balance is None:
        return Response(data = {"message": "pocket_id and balance are required."}, status=HTTP_400_BAD_REQUEST)
    
    try:
        user = Users.objects.get(pocket_id=pocket_id)
        user.balance += dou(balance)
        user.save()
        return Response(data={"message": "Balance updated.", "user": ({
        'id' : user.id,
        'telegram_id': user.telegram_id,
        'pocket_id': user.pocket_id,
        'is_registered': user.is_registered,
        'balance': user.balance,
        'click_id': user.click_id
        })}, status=HTTP_200_OK)
    
    except Users.DoesNotExist:
        return Response(data = {"message": "User not found."}, status=HTTP_404_NOT_FOUND)
    
#__________------------ Views for COURSES, MODULES, LESSONS, EXERCISES ------------__________#



@api_view(['GET'])
def get_courses_info(request):
    if request.method != 'GET':
        return Response(data = {"message": "Method not allowed"}, status=HTTP_405_METHOD_NOT_ALLOWED)
    try:
        courses = Courses.objects.filter(is_published=True)
        Serializer = CoursesSerializer(courses, many = True)
        return Response(data={"message": "Courses found.", "сourses": Serializer.data})
    
    except Courses.DoesNotExist:
        return Response(data = {"message": "Courses not found."}, status=HTTP_404_NOT_FOUND)
    



@api_view(['GET'])
def get_modules_info(request, course_id):
    if request.method != 'GET':
        return Response(data = {"message": "Method not allowed"}, status=HTTP_405_METHOD_NOT_ALLOWED)
    try:
        modules = Modules.objects.filter(course_id=course_id, is_published=True)
        Serializer = ModulesSerializer(modules, many = True)
        return Response(data={"message": "Module found.", "modules": Serializer.data})
    
    except Modules.DoesNotExist:
        return Response(data = {"message": "Modules not found."}, status=HTTP_404_NOT_FOUND)
    



@api_view(['GET'])
def get_lessons_info(request, module_id):
    if request.method != 'GET':
        return Response(data = {"message": "Method not allowed"}, status=HTTP_405_METHOD_NOT_ALLOWED)
    try:
        lessons = Lessons.objects.filter(module_id=module_id, is_published=True)
        Serializer = LessonsSerializer(lessons, many = True)
        return Response(data={"message": "Lessons found.", "lessons": Serializer.data})
    
    except Lessons.DoesNotExist:
        return Response(data = {"message": "Lessons not found."}, status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_exercises_info(request, module_id):
    exercise = Exercises.objects.filter(module_id=module_id, is_published=True).first()

    if not exercise:
        return Response(data={"message": "Exercise not found."}, status=HTTP_404_NOT_FOUND)

   
    serializer = ExercisesSerializer(exercise)
    
    return Response(data={
        "message": "Exercise found.", 
        "exercise": serializer.data
    })



#__________------------ Tradebot View ------------__________#

@api_view(['POST'])
def tradebot(request):
    post_data = request.data
    if not post_data.get('currency_pair') or not post_data.get('timeframe'):
        return Response(data={"message": "currency_pair and timeframe are required."}, status=HTTP_400_BAD_REQUEST)
    if post_data.get("timeframe") not in ["1m", "5m", "15m", "30m", "1h", "4h", "1D"]:
        return Response(data={"message": "Invalid timeframe. Allowed values are: 1m, 5m, 15m, 30m, 1h, 4h, 1D."}, status=HTTP_400_BAD_REQUEST)
    signal, price = get_data(post_data.get('currency_pair'), post_data.get('timeframe'))
    return Response(data={"message": "Signal generated successfully.", "signal": signal, "price": price['close']}, status=HTTP_200_OK)