from django.urls import path
from . import views

urlpatterns = [
    path("admin/", views.index, name="index"),
    path("products/", views.products, name="products"),
    path("products/<int:product_id>/", views.product, name="product"),
    path("auth/login/", views.login, name="login"),


    path('create-newsletter/', views.create_newsletter, name='create_newsletter'),
    path("members/", views.members, name="members"),

    path("admin/user/create/", views.create_user, name="createuser"),
    path("admin/users/get/all/", views.get_users, name="checkusers"),
    path("admin/users/get/by_type", views.get_users_by_type, name="checkmembers"),

    path("users/", views.users, name="users"),
    path("users/members/", views.members, name="members"),

    path('create-newsletter/', views.create_newsletter, name='create_newsletter')
]
