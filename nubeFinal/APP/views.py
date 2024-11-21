from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import boto3
import uuid
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
muebles_table = dynamodb.Table('Muebles')
clientes_table = dynamodb.Table('Clientes')
s3_client = boto3.client('s3')
sns_client = boto3.client('sns', region_name='us-east-1')
BUCKET_NAME = 'practicafinal13'

# Configuración del tópico SNS
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:123456789012:ClientesNotificaciones'  # Reemplazar con el ARN real

#MUEBLES
@csrf_exempt
def crear_mueble(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = Decimal(request.POST.get('precio'))
        stock = int(request.POST.get('stock'))
        
        archivo_imagen = request.FILES.get('foto')
        if archivo_imagen:
            s3_key = f"muebles/{uuid.uuid4()}_{archivo_imagen.name}"
            s3_client.upload_fileobj(archivo_imagen, BUCKET_NAME, s3_key)
            foto_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
        else:
            return JsonResponse({'error': 'Imagen requerida'}, status=400)

        mueble_id = str(uuid.uuid4())
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

#CLIENTES    
@csrf_exempt
def crear_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente_id = str(uuid.uuid4())
            cliente = {
                'cliente_id': cliente_id,
                'nombre': data.get('nombre'),
                'email': data.get('email'),
                'telefono': data.get('telefono'),
                'direccion': data.get('direccion')
            }
            clientes_table.put_item(Item=cliente)
            return JsonResponse({'message': 'Cliente creado exitosamente', 'cliente_id': cliente_id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def obtener_clientes(request):
    if request.method == 'GET':
        try:
            response = clientes_table.scan()
            clientes = response.get('Items', [])
            return JsonResponse(clientes, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def obtener_cliente(request, cliente_id):
    if request.method == 'GET':
        try:
            response = clientes_table.get_item(Key={'cliente_id': cliente_id})
            cliente = response.get('Item')
            if cliente:
                return JsonResponse(cliente, status=200)
            else:
                return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def actualizar_cliente(request, cliente_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            atributos = {key: {'Value': value, 'Action': 'PUT'} for key, value in data.items()}
            clientes_table.update_item(
                Key={'cliente_id': cliente_id},
                AttributeUpdates=atributos
            )
            return JsonResponse({'message': 'Cliente actualizado exitosamente'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def eliminar_cliente(request, cliente_id):
    if request.method == 'DELETE':
        try:
            clientes_table.delete_item(Key={'cliente_id': cliente_id})
            return JsonResponse({'message': 'Cliente eliminado exitosamente'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# Notificaciones con SNS
@csrf_exempt
def enviar_notificacion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mensaje = data.get('mensaje')
            asunto = data.get('asunto', 'Notificación de Casa Diana')

            response = sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=mensaje,
                Subject=asunto
            )
            return JsonResponse({'message': 'Notificación enviada', 'response': response}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def suscribir_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            protocolo = data.get('protocolo')  # "email" o "sms"
            endpoint = data.get('endpoint')

            if protocolo not in ['email', 'sms'] or not endpoint:
                return JsonResponse({'error': 'Protocolo o endpoint inválido'}, status=400)

            response = sns_client.subscribe(
                TopicArn=SNS_TOPIC_ARN,
                Protocol=protocolo,
                Endpoint=endpoint
            )
            return JsonResponse({'message': 'Suscripción exitosa', 'response': response}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)