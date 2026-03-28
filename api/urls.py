from django.urls import path
from .views import CrimeRecordListView, CrimeReportCreateView, PoliceStationListView

urlpatterns = [
    path('crimes/', CrimeRecordListView.as_view(), name='api-crimes'),
    path('reports/', CrimeReportCreateView.as_view(), name='api-reports'),
    path('stations/', PoliceStationListView.as_view(), name='api-stations'),
]
