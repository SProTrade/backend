from django.shortcuts import render, HttpResponse
from users.models import Users  
import json
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED, HTTP_409_CONFLICT
from rest_framework.response import Response
from rest_framework.decorators import api_view
from decimal import Decimal as dou

@api_view(['GET'])
def get_user_info(request):
    if request.method != 'GET':
        return Response(data = {"message": "Method not allowed"}, status=HTTP_405_METHOD_NOT_ALLOWED)
    params = request.GET
    telegram_id = params.get('telegram_id')
    try:
        user = Users.objects.get(telegram_id=telegram_id)
        return Response(data={"message": "User found.", "user": ({
        'id' : str(user.id),
        'telegram_id': user.telegram_id,
        'pocket_id': user.pocket_id,
        'is_registered': user.is_registered,
        'balance': str(user.balance),
        'click_id': user.click_id
        })})
    
    except Users.DoesNotExist:
        return Response(data = {"message": "User not found."}, status=HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
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
        'id' : str(user.id),
        'telegram_id': user.telegram_id,
        'pocket_id': user.pocket_id,
        'is_registered': user.is_registered,
        'balance': str(user.balance),
        'click_id': user.click_id
        })}, status=HTTP_409_CONFLICT)
    
    user = Users.objects.create(telegram_id=telegram_id)
    user.save()
    user.generate_click_id()
    
    return Response(data={"message": "User created.", "user": ({
        'id' : str(user.id),
        'telegram_id': user.telegram_id,
        'pocket_id': user.pocket_id,
        'is_registered': user.is_registered,
        'balance': str(user.balance),
        'click_id': user.click_id,
        'click_id': user.click_id
        })}, status=HTTP_200_OK)



@api_view(['POST'])
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
        'id' : str(user.id),
        'telegram_id': user.telegram_id,
        'pocket_id': user.pocket_id,
        'is_registered': user.is_registered,
        'balance': str(user.balance),
        'click_id': user.click_id
        })}, status=HTTP_200_OK)
    
    except Users.DoesNotExist:
        return Response(data = {"message": "User not found."}, status=HTTP_404_NOT_FOUND)
    


@api_view(['POST'])
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
        'id' : str(user.id),
        'telegram_id': user.telegram_id,
        'pocket_id': user.pocket_id,
        'is_registered': user.is_registered,
        'balance': str(user.balance),
        'click_id': user.click_id
        })}, status=HTTP_200_OK)
    
    except Users.DoesNotExist:
        return Response(data = {"message": "User not found."}, status=HTTP_404_NOT_FOUND)