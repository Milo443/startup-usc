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
from .models import Proyecto, Financiero, Marketing, Producto, Identidad, CargoEmpleado, Feedback
from django.db.models import F,Sum 
from openai import OpenAI

#-------------TEST----------------
from django.test import TestCase, Client
from PIL import ImageGrab
import requests
import requests


key=''

# Create your views here.



def home(request):
        return render(request, 'home.html', {})

#-------------login & register----------------
def signup(request):
        #Si el método de la solicitud es GET, renderiza la página de registro con el formulario de creación de usuario.
        if request.method == 'GET':
                return render(request, 'signup.html', {'form': UserCreationForm})
        else:
                #Obtiene el nombre de usuario, correo electrónico y contraseña del formulario enviado.
                
                username = request.POST['username']
                email = request.POST['email']
                password = request.POST['password1']
                
                #Verifica que ambas contraseñas coincidan.
                if request.POST["password1"] == request.POST["password2"]:
                        try:
                                # Crea un nuevo usuario con las credenciales proporcionadas y lo guarda en la base de datos.
                                user = User.objects.create_user(username=username,email=email,password=password)
                                user.save()
                                # Redirige al usuario a la página de inicio de sesión.
                                return redirect('/login/')
                        except Exception as e:
                                #En caso de error, devuelve el mensaje de excepción.
                                return HttpResponse(e)
                ## Si las contraseñas no coinciden, devuelve un mensaje de error.
                return HttpResponse('Password no es identico')
        #Fin de SignUp

def user_login(request):
        #Si el método de la solicitud es GET, renderiza la página de inicio de sesión con el formulario de autenticación.
        if request.method == 'GET':
                return render(request, 'login.html', {'form': AuthenticationForm})
        else:
                
                #Obtiene el nombre de usuario y la contraseña del formulario enviado.
                #email = request.POST['email']
                username = request.POST['username']
                password = request.POST['password']
                
                #Autentica al usuario con las credenciales proporcionadas.
                user = authenticate(username=username, password=password)
                
                #Si la autenticación es exitosa, verifica si el usuario es personal administrativo.
                if user is not None:
                        staff = user.is_staff
                        
                        #Si el usuario es personal administrativo, redirige a la página del administrador.
                        if staff:
                                return redirect('/administrator/')
                        else:
                                
                                ## Si no es personal administrativo, inicia sesión y redirige a la página principal.
                                login(request, user)
                                return redirect('/main/')
                else:
                        #Si la autenticación falla, muestra un mensaje de error y redirige a la página de inicio de sesión.
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

#-------------ia generador de logo----------------
def generador_logo(request):
        if request.method == 'POST':
                nombre = request.POST.get('nombre')
                descripcion = request.POST.get('descripcion')

        
                client = OpenAI(api_key=key)
                parametro = "a logo for a technology company named " + nombre + " that is modern and techy. description: " + descripcion

                response = client.images.generate(
                model="dall-e-3",
                prompt=parametro,
                size="1024x1024",
                quality="standard",
                n=1,
                )

                image_url = response.data[0].url
                print(image_url)
                return redirect(reverse('crear_proyecto'), {'image_url': image_url})
        else:
                return render(request, 'proyecto/generador_logo.html', {})

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

#-------------FINANCIERO---------------------- 
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
        return render(request, 'proyecto/modulos/financiero/financiero.html', {'proyecto': proyecto, 'financiero': financiero, 'financieros':financieros ,'financiero_exists': financiero_exists,'flujo_caja':flujo_caja, 'ingresos': ingresos, 'egresos': egresos})

def financieros(request):
        financiero = Financiero.objects.all()
        return render(request, 'proyecto/modulos/financiero/financiero.html', {'financiero': financiero})

def form_financiero(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cargo_empleados = CargoEmpleado.objects.filter(proyecto_id=proyecto_id)
        total_salario = CargoEmpleado.objects.aggregate(total_salarios=Sum(F('salario') * F('numero_empleados')))['total_salarios']
        total_salarios = total_salario * 12
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
        return render(request, 'proyecto/modulos/financiero/form_financiero.html', {'proyecto': proyecto, 'cargo_empleados': cargo_empleados, 'total_salarios': total_salarios})

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
        return render(request, 'proyecto/modulos/financiero/edit_financiero.html', {'proyecto': proyecto, 'financiero': financiero})

        #-------------MARKETING----------------
def marketing(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        marketings = Marketing.objects.filter(proyecto_id=proyecto_id)
        marketing_exists = Marketing.objects.filter(proyecto_id=proyecto_id).exists()
        
        nombres = [marketing.mercado_objetivo for marketing in marketings]
        valores = [marketing.gastos_marketing for marketing in marketings]  

        return render(request, 'proyecto/modulos/marketing/marketing.html', {'proyecto': proyecto, 'marketings': marketings, 'marketing_exist': marketing_exists, 'nombres': nombres, 'valores': valores})

def form_marketing(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        if request.method == 'POST':
                mercado_objetivo = request.POST['mercado_objetivo']
                segmentacion_cliente = request.POST['segmentacion_cliente']
                canal_marketing = request.POST['canal_marketing']
                estrategia_precio_promocion = request.POST['estrategia_precio_promocion']
                gastos_marketing = request.POST['gastos_marketing']
                marketing = Marketing(mercado_objetivo=mercado_objetivo, segmentacion_cliente=segmentacion_cliente, canal_marketing=canal_marketing, estrategia_precio_promocion=estrategia_precio_promocion, gastos_marketing=gastos_marketing, proyecto=proyecto)
                marketing.save()
                return redirect(reverse('marketing', args=[proyecto.id]))
        return render(request, 'proyecto/modulos/marketing/form_marketing.html', {'proyecto': proyecto})

def edit_marketing(request, proyecto_id, marketing_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        marketing = Marketing.objects.get(id=marketing_id)
        if request.method == 'POST':
                marketing_id = request.POST['marketing_id']
                marketing.mercado_objetivo = request.POST['mercado_objetivo']
                marketing.segmentacion_cliente = request.POST['segmentacion_cliente']
                marketing.canal_marketing = request.POST['canal_marketing']
                marketing.estrategia_precio_promocion = request.POST['estrategia_precio_promocion']
                marketing.gastos_marketing = request.POST['gastos_marketing']
                marketing.save()
                return redirect(reverse('marketing', args=[proyecto.id]))
        return render(request, 'proyecto/modulos/marketing/edit_marketing.html', {'proyecto': proyecto, 'marketing': marketing})

def delete_marketing(request, proyecto_id, marketing_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        marketing = Marketing.objects.get(id=marketing_id)
        marketing.delete()
        return redirect(reverse('marketing', args=[proyecto.id]))

#-------------PRODUCTO----------------#
def producto(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        producto_exists = Producto.objects.filter(proyecto_id=proyecto_id).exists()
        if producto_exists:
                productos = Producto.objects.get(proyecto_id=proyecto_id)
                productos = Producto.objects.filter(proyecto_id=proyecto_id)
        else:
                productos = None

        return render(request, 'proyecto/modulos/producto/producto.html', {'proyecto': proyecto, 'productos': productos, 'producto_exists': producto_exists})

def form_producto(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        if request.method == 'POST':
                nombre_producto = request.POST['nombre_producto']
                descripcion_producto = request.POST['descripcion_producto']
                categoria_producto = request.POST['categoria_producto']
                ciclo_vida = request.POST['ciclo_vida']
                costo_desarrollo = request.POST['costo_desarrollo']
                costo_produccion = request.POST['costo_produccion']
                precio_venta = request.POST['precio_venta']
                imagen = request.FILES.get('imagen')
                if imagen:
                        producto = Producto(nombre_producto=nombre_producto, descripcion_producto=descripcion_producto, categoria_producto=categoria_producto, ciclo_vida=ciclo_vida, costo_desarrollo=costo_desarrollo, costo_produccion=costo_produccion, precio_venta=precio_venta, imagen=imagen, proyecto=proyecto)
                else:
                        producto = Producto(nombre_producto=nombre_producto, descripcion_producto=descripcion_producto, categoria_producto=categoria_producto, ciclo_vida=ciclo_vida, costo_desarrollo=costo_desarrollo, costo_produccion=costo_produccion, precio_venta=precio_venta, proyecto=proyecto)
                producto.save()
                return redirect(reverse('producto', args=[proyecto.id]))
        return render(request, 'proyecto/modulos/producto/form_producto.html', {'proyecto': proyecto})

def edit_producto(request, proyecto_id, producto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        producto = Producto.objects.get(id=producto_id)
        if request.method == 'POST':
                producto_id = request.POST['producto_id']
                producto.nombre_producto = request.POST['nombre_producto']
                producto.descripcion_producto = request.POST['descripcion_producto']
                producto.categoria_producto = request.POST['categoria_producto']
                producto.ciclo_vida = request.POST['ciclo_vida']
                producto.costo_desarrollo = request.POST['costo_desarrollo']
                producto.costo_produccion = request.POST['costo_produccion']
                producto.precio_venta = request.POST['precio_venta']
                producto.imagen = request.FILES.get('imagen')
                producto.save()
                return redirect(reverse('producto', args=[proyecto.id]))
        return render(request, 'proyecto/modulos/producto/edit_producto.html', {'proyecto': proyecto, 'producto': producto})

def delete_producto(request, proyecto_id, producto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        producto = Producto.objects.get(id=producto_id)
        producto.delete()
        return redirect(reverse('producto', args=[proyecto.id]))

#--------------RECURSOS HUMANOS----------------#
def recursos_humanos(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cargo_exists = CargoEmpleado.objects.filter(proyecto_id=proyecto_id).exists()
        if cargo_exists:
                cargos_empleados = CargoEmpleado.objects.filter(proyecto_id=proyecto_id)
        else:
                cargos_empleados = None
        return render(request, 'proyecto/modulos/recursos_humanos/recursos_humanos.html', {'proyecto': proyecto, 'cargos_empleados': cargos_empleados, 'cargo_exists': cargo_exists})

def form_recursos_humanos(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        if request.method == 'POST':
                nombre_cargo = request.POST['nombre_cargo']
                descripcion_cargo = request.POST['descripcion_cargo']
                requisitos_cargo = request.POST['requisitos_cargo']
                salario = request.POST['salario']
                numero_empleados = request.POST['numero_empleados']
                recursos_humanos = CargoEmpleado(nombre_cargo=nombre_cargo, descripcion_cargo=descripcion_cargo, requisitos_cargo=requisitos_cargo, salario=salario, numero_empleados=numero_empleados, proyecto=proyecto)
                recursos_humanos.save()
                return redirect(reverse('recursos_humanos', args=[proyecto.id]))
        return render(request, 'proyecto/modulos/recursos_humanos/form_recursos_humanos.html', {'proyecto': proyecto})

def edit_recursos_humanos(request, proyecto_id, cargos_empleados_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cargos_empleados = CargoEmpleado.objects.get(id=cargos_empleados_id)
        if request.method == 'POST':
                cargos_empleados.nombre_cargo = request.POST['nombre_cargo']
                cargos_empleados.descripcion_cargo = request.POST['descripcion_cargo']
                cargos_empleados  .requisitos_cargo = request.POST['requisitos_cargo']
                cargos_empleados.salario = request.POST['salario']
                cargos_empleados.numero_empleados = request.POST['numero_empleados']
                cargos_empleados.save()
                return redirect(reverse('recursos_humanos', args=[proyecto.id]))
        
        return render(request, 'proyecto/modulos/recursos_humanos/edit_recursos_humanos.html', {'proyecto': proyecto, 'cargos_empleados': cargos_empleados})



#-------------IDENTIDAD DEL EMPRENDIMIENTO----------------
def identidad(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        identidad_exists = Identidad.objects.filter(proyecto_id=proyecto_id).exists()
        if identidad_exists:
                identidad = Identidad.objects.get(proyecto_id=proyecto_id)
                return render(request, 'proyecto/modulos/identidad/identidad.html', {'proyecto': proyecto, 'identidad_exists': identidad_exists, 'identidad': identidad})
        return render(request, 'proyecto/modulos/identidad/identidad.html', {'proyecto': proyecto, 'identidad_exists': identidad_exists})

def form_identidad(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        if request.method == 'POST':
                mision = request.POST['mision']
                vision = request.POST['vision']
                valores = request.POST['valores']
                objetivos = request.POST['objetivos']
                identidad = Identidad(mision=mision, vision=vision, valores=valores, objetivos=objetivos, proyecto=proyecto)
                identidad.save()
                return redirect(reverse('identidad', args=[proyecto.id]))
        return render(request, 'proyecto/modulos/identidad/form_identidad.html', {'proyecto': proyecto})

def edit_identidad(request, proyecto_id, identidad_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        identidad = Identidad.objects.get(id=identidad_id)
        if request.method == 'POST':
                identidad_id = request.POST['identidad_id']
                identidad.mision = request.POST['mision']
                identidad.vision = request.POST['vision']
                identidad.valores = request.POST['valores']
                identidad.objetivos = request.POST['objetivos']
                identidad.save()
                return redirect(reverse('identidad', args=[proyecto.id]))
        return render(request, 'proyecto/modulos/identidad/edit_identidad.html', {'proyecto': proyecto, 'identidad': identidad})



#-------------ANALISIS----------------#
def analisis(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        financiero = Financiero.objects.get(proyecto_id=proyecto_id)
        marketing_list = Marketing.objects.filter(proyecto_id=proyecto_id)
        producto_list = Producto.objects.filter(proyecto_id=proyecto_id)
        cargos_empleados = CargoEmpleado.objects.filter(proyecto_id=proyecto_id)
        identidad = Identidad.objects.get(proyecto_id=proyecto_id)

        
        feedback_exists = Feedback.objects.filter(proyecto_id=proyecto_id).exists()

        client = OpenAI(api_key=key)

        messages = [
                {"role": "system", "content": "Eres un experto en análisis de emprendimientos emergentes. Por favor, analiza el siguiente emprendimiento, proporciona un análisis detallado, grafica de barras o pastel sobre el analisis y la viabilidad del mismo. las estrcutura de la respuesta debe ser la siguiente: analisis,vibilidad y graficas. nota: es muy importante que me responda en formato html y bootstrap 5 para poder visualizarlo en la pagina web y las graficas pueden ser scripts usando chart para ser visualizadas."},
                {"role": "user", "content": f"\nnombre del emprendimiento:{proyecto.nombre},categoria:{proyecto.categoria}, descripcion:{proyecto.descripcion}"},
                {"role": "user", "content": f"\nidentidad: mision:{identidad.mision}, vision:{identidad.vision}, valores:{identidad.valores}, objetivos:{identidad.objetivos}"},
                {"role": "user", "content": f"\nfinanciero: ventas:{financiero.ventas}, costos de produccion:{financiero.costos_produccion}, gastos administrativos:{financiero.gastos_administrativos}, capital propio:{financiero.capital_propio}, prestamo:{financiero.prestamo}, inversores:{financiero.inversores}"}
        ]

        for marketing in marketing_list:
                messages.append({"role": "user", "content": f"\nmarketing: mercado objetivo:{marketing.mercado_objetivo}, segmentacion de cliente:{marketing.segmentacion_cliente}, canal de marketing:{marketing.canal_marketing}, estrategia de precio y promocion:{marketing.estrategia_precio_promocion}, gastos de marketing:{marketing.gastos_marketing}"})

        for producto in producto_list:
                messages.append({"role": "user", "content": f"\nproducto: nombre del producto:{producto.nombre_producto}, descripcion del producto:{producto.descripcion_producto}, categoria del producto:{producto.categoria_producto}, ciclo de vida del producto:{producto.ciclo_vida}, costo de desarrollo:{producto.costo_desarrollo}, costo de produccion:{producto.costo_produccion}, precio de venta:{producto.precio_venta}"})

        for cargo in cargos_empleados:
                messages.append({"role": "user", "content": f"\nrecursos humanos: nombre del cargo:{cargo.nombre_cargo}, descripcion del cargo:{cargo.descripcion_cargo}, requisitos del cargo:{cargo.requisitos_cargo}, salario:{cargo.salario}, numero de empleados:{cargo.numero_empleados}"})

        if feedback_exists:
                feedback = Feedback.objects.get(proyecto_id=proyecto_id)
                message_content = feedback.analisis
        else:
                completion = client.chat.completions.create(
                        model="gpt-4o",
                        messages=messages
                )
                message_content = completion.choices[0].message.content

        #-------- marketing --------------------
                messages = [
                        {"role": "system", "content": "Eres un experto en análisis de emprendimientos emergentes. Por favor, analiza el siguiente emprendimiento este solo es el modulo de marketing, proporciona una lista de maximo 5 puntos a mejorar de los datos de marketing, nota: es muy importante que la respuesta este dentro de las etiquetas <ul></ul> y cada punto en <li></li> aplicando bootstrap 5 para poder visualizarlo en la pagina web."},
                        
                ]

                for marketing in marketing_list:
                        messages.append({"role": "user", "content": f"\nmarketing: mercado objetivo:{marketing.mercado_objetivo}, segmentacion de cliente:{marketing.segmentacion_cliente}, canal de marketing:{marketing.canal_marketing}, estrategia de precio y promocion:{marketing.estrategia_precio_promocion}, gastos de marketing:{marketing.gastos_marketing}"})

                completion = client.chat.completions.create(
                                model="gpt-4o",
                                messages=messages
                )
                message_content_marketing = completion.choices[0].message.content
        
        #-------- producto --------------------
                messages = [
                        {"role": "system", "content": "Eres un experto en análisis de emprendimientos emergentes. Por favor, analiza el siguiente emprendimiento este solo es el modulo de producto, proporciona una lista de maximo 5 puntos a mejorar de los datos de producto, nota: es muy importante que la respuesta este dentro de las etiquetas <ul></ul> y cada punto en <li></li> aplicando bootstrap 5 para poder visualizarlo en la pagina web."},
                        
                ]

                for producto in producto_list:
                        messages.append({"role": "user", "content": f"\nproducto: nombre del producto:{producto.nombre_producto}, descripcion del producto:{producto.descripcion_producto}, categoria del producto:{producto.categoria_producto}, ciclo de vida del producto:{producto.ciclo_vida}, costo de desarrollo:{producto.costo_desarrollo}, costo de produccion:{producto.costo_produccion}, precio de venta:{producto.precio_venta}"})

                completion = client.chat.completions.create(
                                model="gpt-4o",
                                messages=messages
                )
                message_content_producto = completion.choices[0].message.content

        #-------- recursos humanos --------------------
                messages = [
                        {"role": "system", "content": "Eres un experto en análisis de emprendimientos emergentes. Por favor, analiza el siguiente emprendimiento este solo es el modulo de recursos humanos, proporciona una lista de maximo 5 puntos a mejorar de los datos de recursos humanos, nota: es muy importante que la respuesta este dentro de las etiquetas <ul></ul> y cada punto en <li></li> aplicando bootstrap 5 para poder visualizarlo en la pagina web."},
                        
                ]

                for cargo in cargos_empleados:
                        messages.append({"role": "user", "content": f"\nrecursos humanos: nombre del cargo:{cargo.nombre_cargo}, descripcion del cargo:{cargo.descripcion_cargo}, requisitos del cargo:{cargo.requisitos_cargo}, salario:{cargo.salario}, numero de empleados:{cargo.numero_empleados}"})

                completion = client.chat.completions.create(
                                model="gpt-4o",
                                messages=messages
                )
                message_content_recursos = completion.choices[0].message.content

        #-------- financiero-----------------
                messages = [
                        {"role": "system", "content": "Eres un experto en análisis de emprendimientos emergentes. Por favor, analiza el siguiente emprendimiento este solo es el modulo de financiero, proporciona una lista de maximo 5 puntos a mejorar de los datos de financiero, nota: es muy importante que la respuesta este dentro de las etiquetas <ul></ul> y cada punto en <li></li> aplicando bootstrap 5 para poder visualizarlo en la pagina web."},
                        {"role": "user", "content": f"\nfinanciero: ventas:{financiero.ventas}, costos de produccion:{financiero.costos_produccion}, gastos administrativos:{financiero.gastos_administrativos}, capital propio:{financiero.capital_propio}, prestamo:{financiero.prestamo}, inversores:{financiero.inversores}"}
                ]   

                completion = client.chat.completions.create(
                                model="gpt-4o",
                                messages=messages
                )
                message_content_financiero = completion.choices[0].message.content

                feedback = Feedback(analisis=message_content,marketing=message_content_marketing,producto=message_content_producto,recursos=message_content_recursos,financiero=message_content_financiero ,proyecto=proyecto)
                feedback.save()
                print(message_content)

        return render(request, 'proyecto/modulos/analisis/analisis.html', {'proyecto': proyecto, 'financiero': financiero, 'marketing_list': marketing_list, 'producto_list': producto_list, 'cargos_empleados': cargos_empleados, 'identidad': identidad, 'message_content': message_content, 'feedback': feedback})

def refeedback(request, proyecto_id, feedback_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        financiero = Financiero.objects.get(proyecto_id=proyecto_id)
        marketing_list = Marketing.objects.filter(proyecto_id=proyecto_id)
        producto_list = Producto.objects.filter(proyecto_id=proyecto_id)
        cargos_empleados = CargoEmpleado.objects.filter(proyecto_id=proyecto_id)
        identidad = Identidad.objects.get(proyecto_id=proyecto_id)

        feedback_exists = Feedback.objects.filter(proyecto_id=proyecto_id).exists()

        client = OpenAI(api_key=key)

        messages = [
                {"role": "system", "content": "Eres un experto en análisis de emprendimientos emergentes. Por favor, analiza el siguiente emprendimiento, proporciona un análisis detallado, grafica de barras o pastel sobre el analisis y la viabilidad del mismo. las estrcutura de la respuesta debe ser la siguiente: analisis,vibilidad y graficas. nota: es muy importante que me responda en formato html y bootstrap 5 para poder visualizarlo en la pagina web y las graficas pueden ser scripts usando chart para ser visualizadas."},
                {"role": "user", "content": f"\nnombre del emprendimiento:{proyecto.nombre},categoria:{proyecto.categoria}, descripcion:{proyecto.descripcion}"},
                {"role": "user", "content": f"\nidentidad: mision:{identidad.mision}, vision:{identidad.vision}, valores:{identidad.valores}, objetivos:{identidad.objetivos}"},
                {"role": "user", "content": f"\nfinanciero: ventas:{financiero.ventas}, costos de produccion:{financiero.costos_produccion}, gastos administrativos:{financiero.gastos_administrativos}, capital propio:{financiero.capital_propio}, prestamo:{financiero.prestamo}, inversores:{financiero.inversores}"}
        ]

        for marketing in marketing_list:
                messages.append({"role": "user", "content": f"\nmarketing: mercado objetivo:{marketing.mercado_objetivo}, segmentacion de cliente:{marketing.segmentacion_cliente}, canal de marketing:{marketing.canal_marketing}, estrategia de precio y promocion:{marketing.estrategia_precio_promocion}, gastos de marketing:{marketing.gastos_marketing}"})

        for producto in producto_list:
                messages.append({"role": "user", "content": f"\nproducto: nombre del producto:{producto.nombre_producto}, descripcion del producto:{producto.descripcion_producto}, categoria del producto:{producto.categoria_producto}, ciclo de vida del producto:{producto.ciclo_vida}, costo de desarrollo:{producto.costo_desarrollo}, costo de produccion:{producto.costo_produccion}, precio de venta:{producto.precio_venta}"})

        for cargo in cargos_empleados:
                messages.append({"role": "user", "content": f"\nrecursos humanos: nombre del cargo:{cargo.nombre_cargo}, descripcion del cargo:{cargo.descripcion_cargo}, requisitos del cargo:{cargo.requisitos_cargo}, salario:{cargo.salario}, numero de empleados:{cargo.numero_empleados}"})

       
        completion = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
        )
        message_content = completion.choices[0].message.content

#-------- marketing --------------------
        messages = [
                {"role": "system", "content": "Eres un experto en análisis de emprendimientos emergentes. Por favor, analiza el siguiente emprendimiento este solo es el modulo de marketing, proporciona una lista de maximo 5 puntos a mejorar de los datos de marketing, nota: es muy importante que la respuesta este dentro de las etiquetas <ul></ul> y cada punto en <li></li> aplicando bootstrap 5 para poder visualizarlo en la pagina web."},
                
        ]

        for marketing in marketing_list:
                messages.append({"role": "user", "content": f"\nmarketing: mercado objetivo:{marketing.mercado_objetivo}, segmentacion de cliente:{marketing.segmentacion_cliente}, canal de marketing:{marketing.canal_marketing}, estrategia de precio y promocion:{marketing.estrategia_precio_promocion}, gastos de marketing:{marketing.gastos_marketing}"})

        completion = client.chat.completions.create(
                        model="gpt-4o",
                        messages=messages
        )
        message_content_marketing = completion.choices[0].message.content

#-------- producto --------------------
        messages = [
                {"role": "system", "content": "Eres un experto en análisis de emprendimientos emergentes. Por favor, analiza el siguiente emprendimiento este solo es el modulo de producto, proporciona una lista de maximo 5 puntos a mejorar de los datos de producto, nota: es muy importante que la respuesta este dentro de las etiquetas <ul></ul> y cada punto en <li></li> aplicando bootstrap 5 para poder visualizarlo en la pagina web."},
                
        ]

        for producto in producto_list:
                messages.append({"role": "user", "content": f"\nproducto: nombre del producto:{producto.nombre_producto}, descripcion del producto:{producto.descripcion_producto}, categoria del producto:{producto.categoria_producto}, ciclo de vida del producto:{producto.ciclo_vida}, costo de desarrollo:{producto.costo_desarrollo}, costo de produccion:{producto.costo_produccion}, precio de venta:{producto.precio_venta}"})

        completion = client.chat.completions.create(
                        model="gpt-4o",
                        messages=messages
        )
        message_content_producto = completion.choices[0].message.content

#-------- recursos humanos --------------------
        messages = [
                {"role": "system", "content": "Eres un experto en análisis de emprendimientos emergentes. Por favor, analiza el siguiente emprendimiento este solo es el modulo de recursos humanos, proporciona una lista de maximo 5 puntos a mejorar de los datos de recursos humanos, nota: es muy importante que la respuesta este dentro de las etiquetas <ul></ul> y cada punto en <li></li> aplicando bootstrap 5 para poder visualizarlo en la pagina web."},
                
        ]

        for cargo in cargos_empleados:
                messages.append({"role": "user", "content": f"\nrecursos humanos: nombre del cargo:{cargo.nombre_cargo}, descripcion del cargo:{cargo.descripcion_cargo}, requisitos del cargo:{cargo.requisitos_cargo}, salario:{cargo.salario}, numero de empleados:{cargo.numero_empleados}"})

        completion = client.chat.completions.create(
                        model="gpt-4o",
                        messages=messages
        )
        message_content_recursos = completion.choices[0].message.content

#-------- financiero-----------------
        messages = [
                {"role": "system", "content": "Eres un experto en análisis de emprendimientos emergentes. Por favor, analiza el siguiente emprendimiento este solo es el modulo de financiero, proporciona una lista de maximo 5 puntos a mejorar de los datos de financiero, nota: es muy importante que la respuesta este dentro de las etiquetas <ul></ul> y cada punto en <li></li> aplicando bootstrap 5 para poder visualizarlo en la pagina web."},
                {"role": "user", "content": f"\nfinanciero: ventas:{financiero.ventas}, costos de produccion:{financiero.costos_produccion}, gastos administrativos:{financiero.gastos_administrativos}, capital propio:{financiero.capital_propio}, prestamo:{financiero.prestamo}, inversores:{financiero.inversores}"}
        ]   

        completion = client.chat.completions.create(
                        model="gpt-4o",
                        messages=messages
        )
        message_content_financiero = completion.choices[0].message.content

        feedback = Feedback(analisis=message_content,marketing=message_content_marketing,producto=message_content_producto,recursos=message_content_recursos,financiero=message_content_financiero ,proyecto=proyecto, id=feedback_id)
        feedback.save()
        return redirect(reverse('analisis', args=[proyecto_id]))



def dahsboard(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        financiero = Financiero.objects.get(proyecto_id=proyecto_id)
        marketing_list = Marketing.objects.filter(proyecto_id=proyecto_id)
        producto_list = Producto.objects.filter(proyecto_id=proyecto_id)
        cargos_empleados = CargoEmpleado.objects.filter(proyecto_id=proyecto_id)
        identidad = Identidad.objects.get(proyecto_id=proyecto_id)

        financiero_exists = Financiero.objects.filter(proyecto_id=proyecto_id).exists()
        marketing_exists = Marketing.objects.filter(proyecto_id=proyecto_id).exists()
        producto_exists = Producto.objects.filter(proyecto_id=proyecto_id).exists()
        cargos_empleados_exists = CargoEmpleado.objects.filter(proyecto_id=proyecto_id).exists()

        if financiero_exists and marketing_exists and producto_exists and cargos_empleados_exists:
                modulos_exists = True
        else:
                modulos_exists = False
                
        labels_financiero = ['Ventas', 'Costos de produccion', 'Gastos administrativos', 'Capital propio', 'Prestamo', 'Inversores']
        values_financiero = [financiero.ventas, financiero.costos_produccion, financiero.gastos_administrativos, financiero.capital_propio, financiero.prestamo, financiero.inversores]

        #------marketing----------------
        labels_marketing = []
        
        values_marketing = []
        for marketing in marketing_list:
                labels_marketing.append(marketing.canal_marketing)
                values_marketing.append(marketing.gastos_marketing)

        #------producto----------------
        labels_producto = []
        values_producto = []
        for producto in producto_list:
                labels_producto.append(producto.nombre_producto)
                values_producto.append(producto.precio_venta)
        
        #------recursos humanos----------------
        labels_recursos = []
        values_recursos = []
        for cargo in cargos_empleados:
                labels_recursos.append(cargo.nombre_cargo)
                values_recursos.append(cargo.salario)

        feedback_exists = Feedback.objects.filter(proyecto_id=proyecto_id).exists()
        
        if feedback_exists:
                feedback = Feedback.objects.get(proyecto_id=proyecto_id)
                message_content_marketing = feedback.marketing
                message_content_producto = feedback.producto
                message_content_recursos = feedback.recursos
                message_content_financiero = feedback.financiero
        
        else:
                message_content_marketing = ''
                message_content_producto = ''
                message_content_recursos = ''
                message_content_financiero = ''
                
        
        return render(request, 'proyecto/modulos/dashboard/dashboard.html', {'proyecto': proyecto, 'financiero': financiero, 'marketing_list': marketing_list, 'producto_list': producto_list, 'cargos_empleados': cargos_empleados, 'labels_financiero': labels_financiero, 'values_financiero': values_financiero, 'labels_marketing': labels_marketing, 'values_marketing': values_marketing, 'labels_producto': labels_producto, 'values_producto': values_producto, 'labels_recursos': labels_recursos, 'values_recursos': values_recursos, 'modulos_exists': modulos_exists, 'message_content_marketing': message_content_marketing, 'message_content_producto': message_content_producto, 'message_content_recursos': message_content_recursos, 'message_content_financiero': message_content_financiero})




def asistente_ia(request):
        # Capture screenshot of the current browser window
        screenshot = ImageGrab.grab()

        # Save the screenshot as an image file
        screenshot.save('media/images/screenshot.png')

        # Call the function with the path to the screenshot image
        screenshot_path = "media/images/screenshot.png"
        image_url = upload_image_to_imgbb(screenshot_path)


        client = OpenAI(api_key=key)

        messages=[
        {"role": "system", "content": "eres un asistente virtual, recibiras una screenshot y le indicara de manera muy amigable al usuario que hacer."},
        {"role": "user", "content": f"imagen:{image_url}"}
        ]
        completion = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
        )

        message_content = completion.choices[0].message.content
        print(message_content)

        return redirect('/main/')

def upload_image_to_imgbb(image_path):
        url = "https://api.imgbb.com/1/upload"
        params = {
                "expiration": 600,
                "key": "09a1260d440431ea06ce8e6c723069c6"
        }
        files = {
                "image": open(image_path, "rb")
        }
        response = requests.post(url, params=params, files=files)
        data = response.json()
        image_url = data["data"]["url"]
        print(image_url)
        return image_url



#def analisis(request, proyecto_id):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        financiero = Financiero.objects.get(proyecto_id=proyecto_id)
        marketing_list = Marketing.objects.filter(proyecto_id=proyecto_id)
        producto_list = Producto.objects.filter(proyecto_id=proyecto_id)
        cargos_empleados = CargoEmpleado.objects.filter(proyecto_id=proyecto_id)
        identidad = Identidad.objects.get(proyecto_id=proyecto_id)


        client = OpenAI(api_key=key)

        messages = [
                {"role": "system", "content": "Eres un experto en análisis de emprendimientos emergentes. analiza el siguiente emprendimiento, proporciona un análisis detallado."},
                {"role": "system", "content": "genera graficas de barras y pastel sobre el analisis."},
                {"role": "system", "content": " nota: la respuesta debe ser en formato html. las graficas deben ser scripts usando la libreria chart para ser visualizadas."},
                {"role": "user", "content": f"\nnombre del emprendimiento:{proyecto.nombre},categoria:{proyecto.categoria}, descripcion:{proyecto.descripcion}"},
               {"role": "user", "content": f"\nidentidad: mision:{identidad.mision}, vision:{identidad.vision}, valores:{identidad.valores}, objetivos:{identidad.objetivos}"},
                {"role": "user", "content": f"\nfinanciero: ventas:{financiero.ventas}, costos de produccion:{financiero.costos_produccion}, gastos administrativos:{financiero.gastos_administrativos}, capital propio:{financiero.capital_propio}, prestamo:{financiero.prestamo}, inversores:{financiero.inversores}"}
        ]

        for marketing in marketing_list:
                messages.append({"role": "user", "content": f"\nmarketing: mercado objetivo:{marketing.mercado_objetivo}, segmentacion de cliente:{marketing.segmentacion_cliente}, canal de marketing:{marketing.canal_marketing}, estrategia de precio y promocion:{marketing.estrategia_precio_promocion}, gastos de marketing:{marketing.gastos_marketing}"})

        for producto in producto_list:
                messages.append({"role": "user", "content": f"\nproducto: nombre del producto:{producto.nombre_producto}, descripcion del producto:{producto.descripcion_producto}, categoria del producto:{producto.categoria_producto}, ciclo de vida del producto:{producto.ciclo_vida}, costo de desarrollo:{producto.costo_desarrollo}, costo de produccion:{producto.costo_produccion}, precio de venta:{producto.precio_venta}"})

        for cargo in cargos_empleados:
                messages.append({"role": "user", "content": f"\nrecursos humanos: nombre del cargo:{cargo.nombre_cargo}, descripcion del cargo:{cargo.descripcion_cargo}, requisitos del cargo:{cargo.requisitos_cargo}, salario:{cargo.salario}, numero de empleados:{cargo.numero_empleados}"})

        completion = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
        )

        message_content = completion.choices[0].message.content
        print(message_content)

        return render(request, 'proyecto/modulos/analisis/analisis.html', {'proyecto': proyecto, 'financiero': financiero, 'marketing_list': marketing_list, 'producto_list': producto_list, 'cargos_empleados': cargos_empleados, 'identidad': identidad, 'message_content': message_content})





        
