"""
URL configuration for startup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from emprendimiento import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('', views.home),
    #-----------login & register-----------------
    path('signup/', views.signup),
    path('signup/',views.signup),
    path('login/', views.user_login),
    path('logout/', views.logout),
    #------------admin--------------------
    path('admin/', admin.site.urls),
    path('delete_user_admin/<int:user_id>/', views.delete_user_admin, name='delete_user'),
    path('edit_user_admin/<int:user_id>/', views.edit_user_admin, name='edit_user_admin'),
    path('administrator/', views.administrator),
    #------------proyecto dashboard---------------
    path('main/', views.main),
    path('crear_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    path('eliminar_proyecto/<int:proyecto_id>/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('editar_proyecto/<int:proyecto_id>/', views.editar_proyecto, name='editar_proyecto'),

    #--------------proyecto gestion----------------
    path('gestionar_proyecto/<int:proyecto_id>/', views.gestionar_proyecto, name='gestionar_proyecto'), 
        #--------------financiero----------------
    path('financiero/', views.financieros, name='financiero'),
    path('financiero/<int:proyecto_id>/', views.financiero, name='financiero'),
    path('form_financiero/<int:proyecto_id>/', views.form_financiero, name='form_financiero'),
    path('edit_financiero/<int:proyecto_id>/<int:financiero_id>/', views.edit_financiero, name='edit_financiero'),
        #--------------marketing----------------
    path('marketing/<int:proyecto_id>/', views.marketing, name='marketing'),
    path('form_marketing/<int:proyecto_id>/', views.form_marketing, name='form_marketing'),
    path('edit_marketing/<int:proyecto_id>/<int:marketing_id>/', views.edit_marketing, name='edit_marketing'),
    path('delete_marketing/<int:proyecto_id>/<int:marketing_id>/', views.delete_marketing, name='delete_marketing'),
    #--------------producto----------------
    path('producto/<int:proyecto_id>/', views.producto, name='producto'),
    path('form_producto/<int:proyecto_id>/', views.form_producto, name='form_producto'),
    path('edit_producto/<int:proyecto_id>/<int:producto_id>/', views.edit_producto, name='edit_producto'),
    path('delete_producto/<int:proyecto_id>/<int:producto_id>/', views.delete_producto, name='delete_producto'),
    #--------------identidad----------------
    path('identidad/<int:proyecto_id>/', views.identidad, name='identidad'),
    path('form_identidad/<int:proyecto_id>/', views.form_identidad, name='form_identidad'),
    path('edit_identidad/<int:proyecto_id>/<int:identidad_id>/', views.edit_identidad, name='edit_identidad'),
    #--------------recursos humanos----------------
    path('recursos_humanos/<int:proyecto_id>/', views.recursos_humanos, name='recursos_humanos'),
    path('form_recursos_humanos/<int:proyecto_id>/', views.form_recursos_humanos, name='form_recursos_humanos'),
    path('edit_recursos_humanos/<int:proyecto_id>/<int:cargos_empleados_id>/', views.edit_recursos_humanos, name='edit_recursos_humanos'),


    #--------------analisis-----------------
    path('analisis/<int:proyecto_id>/', views.analisis, name='analisis'),

    #-------------usuario----------------
    path('edit_user/', views.edit_user, name='edit_user'),


    path('asistente_ia/', views.asistente_ia),
    path('generador-logo/', views.generador_logo),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
