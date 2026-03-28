from rest_framework import serializers
from apps.crime_hotspot.models import CrimeRecord, CrimeReport
from apps.sos_system.models import PoliceStation


class CrimeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeRecord
        fields = '__all__'


class CrimeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeReport
        fields = '__all__'


class PoliceStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceStation
        fields = '__all__'
