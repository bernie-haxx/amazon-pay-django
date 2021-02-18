from django.urls import path

from core import views

urlpatterns = [
    path("home/", views.index, name='home'),
    path("cart/", views.cart, name='cart'),
    path("confirm/", views.confirm, name='confirm'),
    path("set/", views.set, name='set'),
    path("get_details/", views.get_details, name='get_details')
]
