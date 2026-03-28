from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.classifier_dashboard,
        name='classifier_dashboard'
    ),

]
