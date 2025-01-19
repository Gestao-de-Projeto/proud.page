from django.urls import path
from . import views

urlpatterns = [
    path("admin/", views.index, name="index"),
    path("auth/login/", views.login, name="login"),
]
