from django.urls import path
from .views import robots_api


urlpatterns = [
    path('robots/', robots_api, name='robots_api'),
]
