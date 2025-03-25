import json

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from requests.adapters import HTTPAdapter

from .models import Book, BookGenre

# Sample books data (for demo)
books_data = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "genres": [BookGenre.FICTION],
        "year": 1925,
        "language": "English",
        "pages": 180,
        "status": "available"
    },
    {
        "id": 2,
        "title": "1984",
        "author": "George Orwell",
        "genres": [BookGenre.FICTION, BookGenre.SCIENCE_FICTION],
        "year": 1949,
        "language": "English",
        "pages": 328,
        "status": "available"
    }
]
next_id = 3


@csrf_exempt
def main_screen(request):
    memory_books = [
        Book(
            id=book["id"],
            title=book["title"],
            author=book["author"],
            genres=book["genres"],
            year=book["year"],
            language=book["language"],
            pages=book["pages"],
            status=book["status"]
        )
        for book in books_data
    ]
    context = {"books": memory_books}
    return render(request, "simple.html", context)


@csrf_exempt
def create_book(request):
    if request.method == "POST":
        try:
            global next_id
            data = json.loads(request.body)
            
            new_book = {
                "id": next_id,
                "title": data["title"],
                "author": data["author"],
                "genres": [BookGenre(genre) for genre in data["genres"]],
                "year": data["year"],
                "language": data["language"],
                "pages": data["pages"],
                "status": data["status"]
            }

            books_data.append(new_book)
            next_id += 1

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Book created successfully",
                    "id": new_book["id"],
                }
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


@csrf_exempt
def update_book(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            book_id = data["id"]

            # Find book in our list
            for book in books_data:
                if book["id"] == book_id:
                    # Only update fields that are present in the request data
                    if "title" in data and data["title"]:
                        book["title"] = data["title"]
                    if "author" in data and data["author"]:
                        book["author"] = data["author"]
                    if "genres" in data and data["genres"]:
                        book["genres"] = [BookGenre(genre) for genre in data["genres"]]
                    if "year" in data and data["year"]:
                        book["year"] = data["year"]
                    if "language" in data and data["language"]:
                        book["language"] = data["language"]
                    if "pages" in data and data["pages"]:
                        book["pages"] = data["pages"]
                    if "status" in data and data["status"]:
                        book["status"] = data["status"]
                    
                    return JsonResponse({
                        "status": "success",
                        "message": "Book updated successfully",
                        "book": book  # Return the updated book data
                    })

            return JsonResponse({"status": "error", "message": "Book not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


def get_books(request):
    if request.method == "GET":
        return JsonResponse(books_data, safe=False)


@csrf_exempt
def get_book(request, book_id):
    if request.method == "GET":
        try:
            for book in books_data:
                if book["id"] == book_id:
                    return JsonResponse({
                        "status": "success",
                        "book": book
                    })
            return JsonResponse({"status": "error", "message": "Book not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


@csrf_exempt
def delete_book(request, book_id):
    if request.method == "DELETE":
        try:
            for i, book in enumerate(books_data):
                if book["id"] == book_id:
                    books_data.pop(i)
                    return JsonResponse({
                        "status": "success",
                        "message": "Book deleted successfully"
                    })
            return JsonResponse({"status": "error", "message": "Book not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


@csrf_exempt
def backend_health_check(request):
    if request.method == "GET":
        try:
            # url = "http://127.0.0.1:8001/version"
            url = "http://backend:8000/version"
            s = requests.Session()
            s.mount(url, HTTPAdapter(max_retries=3))
            backend_status = s.get(url)

            selected_color = "red" if backend_status.status_code != 200 else "green"
            if backend_status.status_code == 200:
                info = json.loads(backend_status.content.decode("utf-8"))
                msg = f"Version: {info['version']}"
            else:
                msg = "Error"

            return JsonResponse({"status": "success", "color": selected_color, "msg": msg})

        except Exception as e:
            print(e)
            return JsonResponse({"status": "success", "color": "red", "msg": "Error"})

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
