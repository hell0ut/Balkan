from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('product/<str:pk>/', views.product, name="product"),
    path('update_item/',views.updateItem,name='update_item')
]