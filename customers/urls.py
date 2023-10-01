from django.urls import path
from customers.views import customers_list


urlpatterns = [
    path('', customers_list, name='customers_list'),
]
