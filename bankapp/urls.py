from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('', mainpage, name = 'homepage'),
    path('signup/', SignUp, name='signup'),
    path('signin/', LoginUser, name='signin'),
    path('logout/', LogOut, name='logout'),
    path('personal/', PersonalPage, name='personal'),
    path('changedata/', UserChangePage, name='userchange'),
    path('sendmoney/', SendMoneyPage, name='sendmoneypage'),
]
