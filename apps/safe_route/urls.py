from django.urls import path
from . import views

urlpatterns = [
    path('', views.route_dashboard, name='route_dashboard'),
]
