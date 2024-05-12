"""
URL configuration for startupDjango project.

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

from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('signup/',views.signup),
    path('login/', views.user_login),
    path('main/', views.main),
    path('logout/', views.logout),
    path('crear_proyecto/', views.crear_proyecto),
    path('administrator/', views.administrator),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]