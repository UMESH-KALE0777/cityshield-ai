from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotspot_dashboard, name='hotspot_dashboard'),
    path('report/', views.report_crime, name='report_crime'),
]
