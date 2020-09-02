'''
Purpose:- Home page define
'''
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



#@login_required
def home(request):
	return HttpResponse('home page')