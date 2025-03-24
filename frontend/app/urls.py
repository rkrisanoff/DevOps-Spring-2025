from django.urls import path

from . import views

urlpatterns = [
    path("", views.main_screen, name="main_screen"),
    path("create_client/", views.create_client, name="create_client"),
    path("update_client/", views.update_client, name="update_client"),
    path("get_clients/", views.get_clients, name="get_clients"),
    path("backend_health_check/", views.backend_health_check, name="backend_health_check"),
]
