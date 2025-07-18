# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import logout as logout_user
from django.contrib.auth import login as login_user
from course.models import *
import os
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from google.oauth2 import id_token
from google.auth.transport import requests
from django.http import JsonResponse
from django.template import loader
from django.conf import settings
from django.contrib.auth.models import User
from . import models
from dotenv import load_dotenv
import json
from django.views.decorators.cache import never_cache
from django.contrib import messages

#loading webpages
def homepage(request):
    return render(request, 'homepage.html')

@login_required
def training(request):
    try:
        return render(request,'training.html')
    except:
        return render(request, 'unauthorized.html')
@never_cache
@login_required
def quiz(request):
    current_user=request.user.validuser
    if current_user.attempt<=15:
        return render(request,'quiz.html')
    else:
        messages.error(request,"Maximum Attempt Exceeded")
        return redirect('/training/section4')
@login_required
def section2(request):
    try:
        return render(request, 'section2.html')
    except:
        return render(request, 'unauthorized.html')
@login_required
def section3(request):
    try:
        return render(request,'section3.html')
    except:
        return render(request, 'unauthorized.html')
@login_required
def section4(request):
    try:
        return render(request, 'section4.html')
    except:
        return render(request, 'unauthorized.html')

@login_required
def certificate(request):
    user = request.user
    validuser = ValidUser.objects.get(user=user)
    context = {'validuser' : validuser}
    if validuser.score >=70:
        return render(request,'certificate.html',context)
    else:
        return render(request, 'unauthorized.html')
@login_required
def statement(request):
    user = request.user
    validuser = ValidUser.objects.get(user=user)
    print(validuser.score)
    if validuser.score >=70:
        return render(request, 'statement.html')
    else:
        return render(request, 'unauthorized.html')
def unauthorized(request):
    return render(request, 'unauthorized.html')

#login
@csrf_exempt
def login(request):
    load_dotenv()
    token=request.POST.get('credential')
    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.getenv("CLIENT_ID")
        )
        email = user_data['email']
        print(email)
        name = user_data['name']
        #note to be approved in this app you must go in admin and add the persons name, email to valid user
        allowed = ValidUser.objects.values_list('email', flat=True)
        print(allowed)
        #once google authenticates login, check that google email is actually in approved user list
        if email in allowed:
            print(allowed)
            #create user if not created
            user,created = User.objects.get_or_create(email=email,defaults={'username':email,'name':name})
            validuser,validcreated = ValidUser.objects.get_or_create(user=user, email=email, name=name)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login_user(request,user)
            return redirect('training')
        else:
            return redirect('unauthorized')
    #invalid token etc
    except ValueError:
        return HttpResponse(status=403)

#logout
def logout_session(request):
    if request.method == 'POST':
        logout_user(request)
        return redirect('homepage')

#load environmental variable "client id"
def getenvvar(request):
    load_dotenv()
    print('request')
    clientid=os.getenv("CLIENT_ID")
    return JsonResponse({'client_id': clientid})

#add quiz score to user, update attempt number
def updatepercent(request):
    print('updatepercent')
    current_user=request.user.validuser
    current_user.score=json.loads(request.body).get('percent')
    print(current_user.score)
    current_user.attempt+=1
    current_user.save()
    return JsonResponse({'status':'success' })

def updateawknowledgement(request):
    print("request recieved")
    current_user=request.user.validuser
    current_user.awknowledge=True
    current_user.save()
    return JsonResponse({'status':'success'})


def updateprogress(request):
    current_user=request.user.validuser
    current_user.progress=json.loads(request.body).get('progress')
    current_user.save()
    return JsonResponse({'status':'success'})
