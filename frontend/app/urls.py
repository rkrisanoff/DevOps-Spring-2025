from django.urls import path

from . import views

urlpatterns = [
    path("", views.main_screen, name="main_screen"),
    path("create_book/", views.create_book, name="create_book"),
    path("update_book/", views.update_book, name="update_book"),
    path("get_books/", views.get_books, name="get_books"),
    path("get_book/<int:book_id>/", views.get_book, name="get_book"),
    path("delete_book/<int:book_id>/", views.delete_book, name="delete_book"),
    path("backend_health_check/", views.backend_health_check, name="backend_health_check"),
    path("frontend_health_check/", views.frontend_health_check, name="frontend_health_check"),
]
