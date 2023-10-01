from django.urls import path
from orders.views import create_order, orders_list


urlpatterns = [
    path('', orders_list, name='orders_list'),
    path('create/', create_order, name='create_order'),
]
