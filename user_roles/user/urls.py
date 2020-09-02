'''
Purpose:- user app url define
'''

from django.urls import path,include

from .views import home

app_name = 'user'

# view route define
urlpatterns = [
    #path('', views.SignUP.as_view(), name='signUP'),
    path('', home, name='home')
]