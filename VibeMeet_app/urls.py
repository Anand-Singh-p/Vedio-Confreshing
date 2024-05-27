# from django.urls import path
# from . import views
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    # path('register/', views.register, name='register'),
    # path('login/', views.login_view, name='login'),


   

    path('meeting/', videocall, name='meeting'),
    path('join/', join_room, name="join_room"),
    path('dashboard/', dash_board, name="dash_board"),
    path('logout/',logout_view, name="logout_view"),
    path('register/' , register_attempt , name="register_attempt"),
    path('accounts/login/' , login_attempt , name="login_attempt"),
    path('token' , token_send , name="token_send"),
    path('success' , success , name='success'),
    path('verify/<auth_token>' , verify , name="verify"),
    path('error' , error_page , name="error"),
    path('password_reset_request/', password_reset_request, name='password_reset_request'),
    path('reset_password/<token>/', reset_password, name='reset_password'),
   
    
   
    #path('join/', join_room, name="join_room"),  # URL for joining a meeting
    


    
    
]