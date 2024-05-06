import streamlit as st
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
import firebase_admin
from firebase_admin import auth, credentials, firestore 
from django.shortcuts import redirect

# Create your views here.
def home(request):
    
    return  render(request,'home.html',{
        
    })

def initialize():
        #se corre servicio de auth de firebase y se verifica si el servicio ya esta ejecutado o no
        credential = credentials.Certificate('startup-usc-eee3f6cf1d92.json')
        try:
            default_app = firebase_admin.get_app()

        except:
            firebase_admin.initialize_app(credential)
initialize()

def signup(request):
    #title = 'signup'
    if request.method == 'GET':
        return  render(request,'signup.html',{
        'form':UserCreationForm
    })
    else:
        if request.POST["password1"] == request.POST["password2"]:
            #register usuario
            try:
                #user = User.objects.create_user(username=request.POST['username'],
                #password = request.POST['password1'])
                #user.save()
                
                user = auth.create_user(
                    uid=request.POST['username'],
                    email=request.POST['email'],
                    email_verified=False,
                    password=request.POST['password1'],
                    display_name=request.POST['username']
                )

                return render(request, 'login.html', {
                    'form': AuthenticationForm,
                    'message': 'Usuario creado satisfactoriamente'
                })
            except Exception as e:
                return HttpResponse(e)
        return HttpResponse('Password no es identico')
    
     
def login(request):
    #title = 'login'
    if request.method == 'GET':
        return  render(request,'login.html',{
        'form':AuthenticationForm
    })
    else:
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = auth.get_user_by_email(email)
            if not user.email_verified:
                try:
                    auth.get_user_by_email(email)
                    return redirect('/main/')
                except Exception as e:
                    return HttpResponse(e)
            else:
                return HttpResponse('Correo no verificado')
        except Exception as e:
            return HttpResponse(e)
        
def crearProyecto(request):
    return  render(request,'main.html',{
        
    })