import json
from datetime import datetime

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from requests.adapters import HTTPAdapter

from .models import Client

# Список клиентов (вне БД, для демо)
clients_data = [
    {
        "name": "John Doe",
        "quantity": 5,
        "created_at": "2024-03-20 10:30:00",
        "updated_at": "2024-03-20 10:30:00",
        "id": 1
    },
    {
        "name": "Jane Smith",
        "quantity": 3,
        "created_at": "2024-03-20 11:15:00",
        "updated_at": "2024-03-20 11:15:00",
        "id": 2
    }
]
next_id = 3  


@csrf_exempt
def main_screen(request):
    # по умолчанию клииенты все равно рендерятся в таблице, 
    # чтобы при начале работы таблица содержала значения
    memory_clients = [
        Client(
            id=client["id"],
            name=client["name"],
            quantity=client["quantity"],
            created_at=datetime.strptime(client["created_at"], '%Y-%m-%d %H:%M:%S'),
            updated_at=datetime.strptime(client["updated_at"], '%Y-%m-%d %H:%M:%S')
        ) 
        for client in clients_data
    ]
    context = {
        'clients': memory_clients
    }
    return render(request, 'simple.html', context)


@csrf_exempt
def create_client(request):
    if request.method == 'POST':
        try:
            global next_id
            data = json.loads(request.body)
            print(data)
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            new_client = {
                "id": next_id,
                "name": data['name'],
                "quantity": data['quantity'],
                "created_at": current_time,
                "updated_at": current_time
            }
            
            clients_data.append(new_client)
            next_id += 1
            
            return JsonResponse({
                'status': 'success',
                'message': 'Client created successfully',
                'id': new_client['id']
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)



@csrf_exempt
def update_client(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            client_id = data['id']
            
            # Find client in our list
            for client in clients_data:
                if client['id'] == client_id:
                    client['name'] = data['name']
                    client['quantity'] = data['quantity']
                    client['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Client updated successfully'
                    })
            
            return JsonResponse({
                'status': 'error',
                'message': 'Client not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def get_clients(request):
    if request.method == 'GET':
        return JsonResponse(clients_data, safe=False)


@csrf_exempt
def backend_health_check(request):
    if request.method == 'GET':
        try:
            # url = "http://127.0.0.1:8001/version"
            url= "http://backend:8000/version"
            s = requests.Session()
            s.mount(url, HTTPAdapter(max_retries=3))
            backend_status = s.get(url)

            selected_color = 'red' if backend_status.status_code != 200 else 'green'
            if backend_status.status_code == 200:   
                info = json.loads(
                    backend_status.content.decode('utf-8')
                )
                msg = f"Version: {info['version']}"
            else: 
                msg = 'Error'

            return JsonResponse({
                'status': 'success',
                'color': selected_color,
                'msg': msg
            })
        
        except Exception as e:
            print(e)
            return JsonResponse({
                'status': 'success',
                'color': "red",
                'msg': 'Error'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)