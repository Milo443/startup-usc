
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, logout as auth_logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User

# Create your views here.
def home(request):
        return render(request, 'home.html', {})

def signup(request):
        if request.method == 'GET':
                return render(request, 'signup.html', {'form': UserCreationForm})
        else:
                username = request.POST['username']
                email = request.POST['email']
                password = request.POST['password1']
                if request.POST["password1"] == request.POST["password2"]:
                        try:
                                user = User.objects.create_user(username=username,email=email,password=password)
                                user.save()
                                return redirect('/login/')
                        except Exception as e:
                                return HttpResponse(e)
                return HttpResponse('Password no es identico')

def user_login(request):
        if request.method == 'GET':
                return render(request, 'login.html', {'form': AuthenticationForm})
        else:
                #email = request.POST['email']
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                        staff = user.is_staff
                        if staff:
                                return redirect('/administrator/')
                        else:
                                login(request, user)
                                return redirect('/main/')
                else:
                        messages.error(request, 'Usuario o contraseña incorrecta')
                        return redirect('/login/')

def main(request):
        user_login = request.user
        if user_login.is_authenticated:
                username = user_login.username
                user = User.objects.get(username=username)
                return render(request, 'main.html', {})
        else:
                return HttpResponse('Usuario no autenticado')


def crear_proyecto(request):
        if request.method == 'POST':
                nombre = request.POST['nombre']
                descripcion = request.POST['descripcion']
                categoria = request.POST['categoria']
                imagen = request.FILES['imagen']
                # Assuming you have a model called 'Proyecto' in your models.py file

                return redirect('/main/')
        return render(request, 'components/form_proyecto.html', {})

def logout(request):
        auth_logout(request)
        return redirect('/login/')

def administrator(request):
        users = User.objects.all()
        return render(request, 'admin.html', {'users': users})

def delete_user(request, user_id):
        try:
                user = User.objects.get(id=user_id)
                user.delete()
                messages.success(request, 'Usuario eliminado con éxito.')
                return redirect('/administrator/')
        except User.DoesNotExist:
                return HttpResponse('Usuario no encontrado')