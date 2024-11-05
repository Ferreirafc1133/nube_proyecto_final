# nubeFinal/urls.py
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mueble/', views.crear_mueble, name='crear_mueble'),
    path('muebles/', views.obtener_muebles, name='crear_mueble'),
    path('mueble/<str:mueble_id>/', views.obtener_mueble, name='obtener_mueble'),
    path('mueble/<str:mueble_id>/actualizar/', views.actualizar_mueble, name='actualizar_mueble'), 
    path('mueble/<str:mueble_id>/eliminar/', views.eliminar_mueble, name='eliminar_mueble'),
]
