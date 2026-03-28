from rest_framework import generics, permissions
from apps.crime_hotspot.models import CrimeRecord, CrimeReport
from apps.sos_system.models import PoliceStation
from .serializers import CrimeRecordSerializer, CrimeReportSerializer, PoliceStationSerializer


class CrimeRecordListView(generics.ListAPIView):
    queryset = CrimeRecord.objects.all().order_by('-date')
    serializer_class = CrimeRecordSerializer
    permission_classes = [permissions.IsAuthenticated]


class CrimeReportCreateView(generics.CreateAPIView):
    queryset = CrimeReport.objects.all()
    serializer_class = CrimeReportSerializer
    permission_classes = [permissions.IsAuthenticated]


class PoliceStationListView(generics.ListAPIView):
    queryset = PoliceStation.objects.all()
    serializer_class = PoliceStationSerializer
    permission_classes = [permissions.IsAuthenticated]
