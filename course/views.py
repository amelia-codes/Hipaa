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

def homepage(request):
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render())
@login_required
def training(request):
    print('trying to load')
    template = loader.get_template('training.html')
    return render(request,'training.html')
@never_cache
@login_required
def quiz(request):
    template = loader.get_template('quiz.html')
    questions = Ques.objects.all()
    current_user=request.user.validuser
    if current_user.attempt<=2:
        return render(request,'quiz.html')
    else:
        return HttpResponse('Maximum attempts exceeded')
@login_required
def section2(request):
    template = loader.get_template('section2.php')
    return HttpResponse(template.render())
@login_required
def section3(request):
    #template = loader.get_template('section3.html')
    return render(request,'section3.html')
@login_required
def section4(request):
    template = loader.get_template('section4.html')
    return HttpResponse(template.render())
@login_required
def section5(request):
    template = loader.get_template('section5.html')
    return HttpResponse(template.render())
@login_required
def certificate(request):
    template = loader.get_template('certificate.html')
    return HttpResponse(template.render())
@login_required
def statement(request):
    template = loader.get_template('statement.html')
    return HttpResponse(template.render())
def unauthorized(request):
    template = loader.get_template('unauthorized.html')
    return HttpResponse(template.render())

@csrf_exempt
def login(request):
    load_dotenv()
    print('requestattempt')
    token=request.POST.get('credential')
    try:
        print("login")
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.getenv("CLIENT_ID")
        )
        email = user_data['email']
        name = user_data['name']
        print(name)
        print(email)
        allowed = ValidUser.objects.values_list('email', flat=True)
        if email in allowed:
            print(allowed)
            request.session['username'] = email
            #save email as user id to database and attach score
            user,created = User.objects.get_or_create(email=email,defaults={'username':email,'name':name})
            print('almostvaliduser')
            validuser,validcreated = ValidUser.objects.get_or_create(user=user, email=email, name=name)
            print('validuser')
            user.backend = 'django.contrib.auth.backends.ModelBackend' #figure out later
            print('loading')
            login_user(request,user)
            print('done')
            return redirect('training')
        else:
            return redirect('unauthorized')
    except ValueError:
        return HttpResponse(status=403)

def logout_session(request):
    if request.method == 'POST':
        print('logout')
        current_user=request.user.validuser
        logout_user(request)
        print('i think it works?')
        return redirect('homepage')
def getenvvar(request):
    load_dotenv()
    print('request')
    clientid=os.getenv("CLIENT_ID")
    return JsonResponse({'client_id': clientid})

def updatepercent(request):
    print('updatepercent')
    current_user=request.user.validuser
    current_user.score=json.loads(request.body).get('percent')
    #current_user.score=request.POST.get('percent')#make it so can't access quiz again
    print(current_user.score)
    current_user.attempt+=1
    current_user.save()
    return JsonResponse({'status':'success' })

#def updateprogress(request):
#    user.progress+=0#someamount
#    user.save()
