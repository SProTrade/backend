from django.urls import path, include
from . import views

urlpatterns = [
    path('user/', views.get_user_info, name='get_user_info'),
    path('user/create/', views.create_user, name='create_user'),
    path('user/poid/', views.update_user_pocketid, name='update_user_pocket_id'),
    path('user/balance/', views.update_user_balance, name='update_user_balance'),
]