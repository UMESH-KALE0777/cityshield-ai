from django.test import TestCase
from apps.crime_hotspot.models import CrimeRecord, CrimeReport
from apps.sos_system.models import PoliceStation
from apps.sos_system.services import haversine_km, find_nearest_station
import datetime


class CrimeRecordModelTest(TestCase):
    def test_str(self):
        r = CrimeRecord(crime_type='Theft', area='MG Road')
        self.assertEqual(str(r), 'Theft at MG Road')


class HaversineTest(TestCase):
    def test_same_point_is_zero(self):
        self.assertAlmostEqual(haversine_km(12.97, 77.59, 12.97, 77.59), 0.0, places=2)

    def test_known_distance(self):
        # Bangalore to Mysore ≈ 128 km (straight line)
        dist = haversine_km(12.9716, 77.5946, 12.2958, 76.6394)
        self.assertGreater(dist, 120)
        self.assertLess(dist, 160)


class FindNearestStationTest(TestCase):
    def setUp(self):
        PoliceStation.objects.create(name='Central PS', latitude=12.9716, longitude=77.5946, address='Central')
        PoliceStation.objects.create(name='Far PS', latitude=13.5, longitude=78.0, address='Far')

    def test_finds_nearest(self):
        station, dist = find_nearest_station(12.97, 77.59)
        self.assertEqual(station.name, 'Central PS')
        self.assertLess(dist, 1.0)