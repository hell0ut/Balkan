from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('update_item/',views.updateItem,name='update_item'),
    path('delivery/',views.delivery,name='delivery'),
    path('privacypolicy/',views.privacy_policy,name='privacy_policy'),
    path('my-ajax-test/', views.myajaxtestview, name='ajax-test-view'),
]