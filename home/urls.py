from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('update_item/',views.updateItem,name='update_item'),
    path('delivery/',views.delivery,name='delivery'),
    path('privacypolicy/',views.privacy_policy,name='privacy_policy'),
]