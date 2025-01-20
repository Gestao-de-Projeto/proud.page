from django.urls import path
from . import views

urlpatterns = [
    path("admin/", views.index, name="index"),
    path("products/", views.products, name="products"),
    path("products/<int:product_id>/", views.product, name="product"),
    path("auth/login/", views.login, name="login"),
    path('create-newsletter/', views.create_newsletter, name='create_newsletter')
]
