from django.contrib import admin
from .models import CrimeRecord, CrimeReport

@admin.register(CrimeRecord)
class CrimeRecordAdmin(admin.ModelAdmin):
    list_display = ('crime_type', 'area', 'date', 'time')
    search_fields = ('crime_type', 'area')

@admin.register(CrimeReport)
class CrimeReportAdmin(admin.ModelAdmin):
    list_display = ('crime_type', 'latitude', 'longitude', 'created_at')
    search_fields = ('crime_type', 'description')
    list_filter = ('crime_type',)
