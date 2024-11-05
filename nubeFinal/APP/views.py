from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import boto3
import uuid
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
muebles_table = dynamodb.Table('Muebles')
s3_client = boto3.client('s3')
BUCKET_NAME = 'practicafinal13'

@csrf_exempt
def crear_mueble(request):
    if request.method == 'POST':
        mueble_id = str(uuid.uuid4())
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = Decimal(str(request.POST.get('precio')))
        stock = int(request.POST.get('stock'))
        foto = request.FILES.get('foto') 

        if foto:
            foto_key = f"muebles/{mueble_id}/{foto.name}"
            s3_client.upload_fileobj(foto, BUCKET_NAME, foto_key, ExtraArgs={'ACL': 'public-read'})
            foto_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{foto_key}"
        else:
            foto_url = None

        muebles_table.put_item(Item={
            'mueble_id': mueble_id,
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': precio,
            'stock': stock,
            'foto_url': foto_url
        })

        return JsonResponse({'message': 'Mueble creado exitosamente', 'mueble_id': mueble_id, 'foto_url': foto_url}, status=201)
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
