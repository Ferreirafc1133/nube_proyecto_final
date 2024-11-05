from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
muebles_table = dynamodb.Table('Muebles')

@csrf_exempt
def crear_mueble(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mueble_id = data.get('mueble_id', str(uuid.uuid4()))
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        precio = float(data.get('precio'))
        stock = int(data.get('stock'))
        foto_url = data.get('foto_url')

        muebles_table.put_item(Item={
            'mueble_id': mueble_id,
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': precio,
            'stock': stock,
            'foto_url': foto_url
        })
        return JsonResponse({'message': 'Mueble creado exitosamente', 'mueble_id': mueble_id}, status=201)

@csrf_exempt
def obtener_muebles(request):
    if request.method == 'GET':
        response = muebles_table.scan()  # Esto devuelve todos los elementos de la tabla
        muebles = response.get('Items', [])
        return JsonResponse(muebles, safe=False)

@csrf_exempt
def obtener_mueble(request, mueble_id):
    if request.method == 'GET':
        response = muebles_table.get_item(Key={'mueble_id': mueble_id})
        mueble = response.get('Item')
        if mueble:
            return JsonResponse(mueble)
        else:
            return JsonResponse({'error': 'Mueble no encontrado'}, status=404)

@csrf_exempt
def actualizar_mueble(request, mueble_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        atributos = {}
        if 'descripcion' in data:
            atributos['descripcion'] = {'Value': data['descripcion'], 'Action': 'PUT'}
        if 'precio' in data:
            atributos['precio'] = {'Value': float(data['precio']), 'Action': 'PUT'}
        if 'stock' in data:
            atributos['stock'] = {'Value': int(data['stock']), 'Action': 'PUT'}
        if 'foto_url' in data:
            atributos['foto_url'] = {'Value': data['foto_url'], 'Action': 'PUT'}

        if atributos:
            muebles_table.update_item(
                Key={'mueble_id': mueble_id},
                AttributeUpdates=atributos
            )
            return JsonResponse({'message': 'Mueble actualizado exitosamente'})
        else:
            return JsonResponse({'error': 'No se proporcionaron campos para actualizar'}, status=400)

@csrf_exempt
def eliminar_mueble(request, mueble_id):
    if request.method == 'DELETE':
        muebles_table.delete_item(Key={'mueble_id': mueble_id})
        return JsonResponse({'message': 'Mueble eliminado exitosamente'})
