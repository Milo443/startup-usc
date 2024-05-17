from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, logout as auth_logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse
import os
from .models import Proyecto, Financiero, Marketing
import requests
from django.db.models import F,Sum 

# Create your views here.
def home(request):
        return render(request, 'home.html', {})

#-------------login & register----------------
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
def logout(request):
        auth_logout(request)
        return redirect('/login/')

#-------------ADMINISTRADOR----------------
def administrator(request):
        users = User.objects.all()
        return render(request, 'admin/admin.html', {'users': users})

def delete_user_admin(request, user_id):
        try:
                user = User.objects.get(id=user_id)
                user.delete()
                messages.success(request, 'Usuario eliminado con éxito.')
                return redirect('/administrator/')
        except User.DoesNotExist:
                return HttpResponse('Usuario no encontrado')

def edit_user_admin(request, user_id):
        user = User.objects.get(id=user_id)
        return render(request, 'admin/edit_user_admin.html', {'user': user})

#-------------USUARIO---------------------------
def edit_user(request):
        user_login = request.user
        if request.method == 'POST':
                user_id = request.POST['user_id']
                user = User.objects.get(id=user_id)
                user.username = request.POST['username']
                user.email = request.POST['email']
                user.set_password(request.POST['password'])
                user.save()
                return redirect('/login/')
        return render(request, 'user/edit_user.html', {})


#-------------PROYECTO DASHBOARD----------------

def main(request):
        user_login = request.user
        if user_login.is_authenticated:
                user = User.objects.get(id=user_login.id)
                proyectos = Proyecto.objects.filter(user=user)
                return render(request, 'main.html', {'proyectos': proyectos})

        else:
                
                return HttpResponse('Usuario no autenticado')


def crear_proyecto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        categoria = request.POST['categoria']
        imagen = request.FILES.get('imagen')  # Usa .get() en lugar de ['imagen']
        if imagen:  # Verifica si se proporcionó una imagen
            proyecto = Proyecto(nombre=nombre, descripcion=descripcion, categoria=categoria, imagen=imagen, user=request.user)
        else:
            proyecto = Proyecto(nombre=nombre, descripcion=descripcion, categoria=categoria, user=request.user)
        proyecto.save()
        return redirect('/main/')
    return render(request, 'proyecto/form_proyecto.html', {})

def editar_proyecto(request, proyecto_id):
        user_login = request.user
        if user_login.is_authenticated:
                user = User.objects.get(id=user_login.id)
                proyecto = Proyecto.objects.get(id=proyecto_id)
                if request.method == 'POST':
                        proyecto_id = request.POST['proyecto_id']
                        proyecto.nombre = request.POST['nombre']
                        proyecto.descripcion = request.POST['descripcion']
                        proyecto.categoria = request.POST['categoria']
                        proyecto.save()
                        return redirect('/main/')
                return render(request, 'proyecto/editar_proyecto.html', {'proyecto': proyecto})

def eliminar_proyecto(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        proyecto.delete()
        return redirect('/main/')


#-------------GESTION DE PROYECTO----------------
def gestionar_proyecto(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        return render(request, 'proyecto/gestionar_proyecto.html', {'proyecto': proyecto})

   #-------------financiero--------------- 
def financiero(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        financieros = Financiero.objects.filter(proyecto_id=proyecto_id)
        financiero_exists = Financiero.objects.filter(proyecto_id=proyecto_id).exists()
        if financiero_exists:
                financiero = Financiero.objects.get(proyecto_id=proyecto_id)
                flujo_caja = financiero.ventas + financiero.capital_propio + financiero.inversores + financiero.prestamo - financiero.costos_produccion - financiero.gastos_administrativos
                ingresos = financiero.ventas + financiero.capital_propio + financiero.inversores + financiero.prestamo
                egresos = financiero.costos_produccion + financiero.gastos_administrativos

        else:
                financiero = None
                flujo_caja = None
                ingresos = None
                egresos = None
        return render(request, 'proyecto/modulos/financiero.html', {'proyecto': proyecto, 'financiero': financiero, 'financieros':financieros ,'financiero_exists': financiero_exists,'flujo_caja':flujo_caja, 'ingresos': ingresos, 'egresos': egresos})

def financieros(request):
        financiero = Financiero.objects.all()
        return render(request, 'proyecto/modulos/financiero.html', {'financiero': financiero})

def form_financiero(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        if request.method == 'POST':
                #proyecto_id = request.POST['proyecto_id']
                #proyecto = Proyecto.objects.get(id=proyecto_id)
                ventas = request.POST['ventas']
                costos_produccion = request.POST['costos_produccion']
                gastos_administrativos = request.POST['gastos_administrativos']
                capital_propio = request.POST['capital_propio']
                prestamo = request.POST['prestamo']
                inversores = request.POST['inversores']
                financiero = Financiero(proyecto=proyecto, ventas=ventas, costos_produccion=costos_produccion, gastos_administrativos=gastos_administrativos, capital_propio=capital_propio, prestamo=prestamo, inversores=inversores)
                financiero.save()
                return redirect(reverse('financiero', args=[proyecto.id]))
        return render(request, 'proyecto/modulos/form_financiero.html', {'proyecto': proyecto})

def edit_financiero(request, proyecto_id, financiero_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        financiero = Financiero.objects.get(id=financiero_id)

        if request.method == 'POST':
                financiero_id = request.POST['financiero_id']
                financiero.ventas = request.POST['ventas']
                financiero.costos_produccion = request.POST['costos_produccion']
                financiero.gastos_administrativos = request.POST['gastos_administrativos']
                financiero.capital_propio = request.POST['capital_propio']
                financiero.prestamo = request.POST['prestamo']
                financiero.inversores = request.POST['inversores']
                financiero.save()
                return redirect(reverse('financiero', args=[proyecto.id]))
        return render(request, 'proyecto/modulos/edit_financiero.html', {'proyecto': proyecto, 'financiero': financiero})

        #-------------MARKETING----------------
def marketing(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        return render(request, 'proyecto/modulos/marketing.html', {'proyecto': proyecto})

def form_marketing(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        if request.method == 'POST':
                mercado_objetivo = request.POST['mercado_objetivo']
                segmentacion_cliente = request.POST['segmentacion_cliente']
                canal_marketing = request.POST['canal_marketing']
                estrategia_precio_promocion = request.POST['estrategia_precio_promocion']
                marketing = Marketing(mercado_objetivo=mercado_objetivo, segmentacion_cliente=segmentacion_cliente, canal_marketing=canal_marketing, estrategia_precio_promocion=estrategia_precio_promocion, proyecto=proyecto)
                marketing.save()
                return redirect(reverse('marketing', args=[proyecto.id]))
        return render(request, 'proyecto/modulos/form_marketing.html', {'proyecto': proyecto})
