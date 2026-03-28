from apps.crime_hotspot.models import CrimeRecord
from django.db.models import Count

total = CrimeRecord.objects.count()
print(f"Total: {total}")

dupes = CrimeRecord.objects.values('latitude', 'longitude').annotate(n=Count('id')).order_by('-n')[:10]
print("Top 10 coordinate pairs by frequency:")
for d in dupes:
    print(d)
