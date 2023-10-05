from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('user/product', views.get_full_user_products, name='get_full_user_products'),
    path('user/lesson', views.get_user_lesson_by_product, name='get_user_lesson_by_product'),
    path('products/', views.get_all_products, name='get_all_products')
]