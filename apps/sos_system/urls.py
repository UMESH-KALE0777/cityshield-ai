from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.sos_dashboard,
        name='sos_dashboard'
    ),

]
