# nubeFinal/urls.py
from django.contrib import admin
from django.urls import path
from APP import views

urlpatterns = [
    #MUEBLES
    path('admin/', admin.site.urls),
    path('mueble/', views.crear_mueble, name='crear_mueble'),
    path('muebles/', views.obtener_muebles, name='crear_mueble'),
    path('mueble/<str:mueble_id>/', views.obtener_mueble, name='obtener_mueble'),
    path('mueble/<str:mueble_id>/actualizar/', views.actualizar_mueble, name='actualizar_mueble'), 
    path('mueble/<str:mueble_id>/eliminar/', views.eliminar_mueble, name='eliminar_mueble'),
    #CLIENTES
    path('clientes/', views.obtener_clientes, name='obtener_clientes'),
    path('clientes/<str:cliente_id>/', views.obtener_cliente, name='obtener_cliente'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/actualizar/<str:cliente_id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/eliminar/<str:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    #SNS
    path('notificaciones/enviar/', views.enviar_notificacion, name='enviar_notificacion'),
    path('notificaciones/suscribir/', views.suscribir_cliente, name='suscribir_cliente'),
]
