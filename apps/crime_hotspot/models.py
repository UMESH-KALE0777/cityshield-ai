from django.db import models

class CrimeRecord(models.Model):
    crime_type = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    area = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.crime_type} at {self.area}"

class CrimeReport(models.Model):

    crime_type = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crime_type} - {self.description[:20]}"
