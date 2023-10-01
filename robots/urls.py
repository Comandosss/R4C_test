from django.urls import path
from robots.views import robots_list, add_robot


urlpatterns = [
    path('', robots_list, name='robots_list'),
    path('add_robot/', add_robot, name='add_robot'),
]
