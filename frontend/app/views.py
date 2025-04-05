import json

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from requests.adapters import HTTPAdapter

# BACKEND_URL = "127.0.0.1"
# BACKEND_PORT = "8001"

BACKEND_URL = "backend"
BACKEND_PORT = "8000"


@csrf_exempt
def main_screen(request):
    return render(request, "simple.html", {"books": []})


@csrf_exempt
def create_book(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            response = requests.post(f"http://{BACKEND_URL}:{BACKEND_PORT}/api/books", json=data)
            if response.status_code == 200:
                result = response.json()
                return JsonResponse(result)
            else:
                return JsonResponse({}, status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


@csrf_exempt
def update_book(request):
    if request.method == "PATCH":
        try:
            data = json.loads(request.body.decode("utf-8"))
            response = requests.patch(
                f"http://{BACKEND_URL}:{BACKEND_PORT}/api/books/{data['id']}", json=data
            )
            if response.status_code == 200:
                result = response.json()
                return JsonResponse(result)
            else:
                return JsonResponse({}, status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


def get_books(request):
    if request.method == "GET":
        try:
            response = requests.get(f"http://{BACKEND_URL}:{BACKEND_PORT}/api/books/")
            if response.status_code == 200:
                data = response.json()
                return JsonResponse(data)
            else:
                return JsonResponse({}, status=response.status_code)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({}, status=405)


@csrf_exempt
def get_book(request, book_id):
    if request.method == "GET":
        try:
            response = requests.get(f"http://{BACKEND_URL}:{BACKEND_PORT}/api/books/{book_id}")
            if response.status_code == 200:
                data = response.json()
                return JsonResponse(data)

            else:
                return JsonResponse({}, status=response.status_code)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({}, status=405)


@csrf_exempt
def delete_book(request, book_id):
    if request.method == "DELETE":
        try:
            response = requests.delete(f"http://{BACKEND_URL}:{BACKEND_PORT}/api/books/{book_id}")
            return JsonResponse({}, status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


@csrf_exempt
def backend_health_check(request):
    if request.method == "GET":
        try:
            url = f"http://{BACKEND_URL}:{BACKEND_PORT}/version"
            s = requests.Session()
            s.mount(url, HTTPAdapter(max_retries=3))
            backend_status = s.get(url)
            if backend_status.status_code == 200:
                data = backend_status.json()
            else:
                data = {"version": "0"}
            return JsonResponse(data, status=backend_status.status_code)

        except Exception:
            return JsonResponse({}, status=500)

    return JsonResponse({}, status=405)


@csrf_exempt
def frontend_health_check(request):
    return JsonResponse({"version": "0.1.0"}, status=200)
