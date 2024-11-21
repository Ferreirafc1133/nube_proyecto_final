from django.db import models
class Mueble:
    def __init__(self, nombre, descripcion, precio, stock, foto_url):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.foto_url = foto_url

    def __str__(self):
        return self.nombre

class Cliente:
    def __init__(self, cliente_id, nombre, email, telefono, direccion):
        self.cliente_id = cliente_id
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        return self.nombre
