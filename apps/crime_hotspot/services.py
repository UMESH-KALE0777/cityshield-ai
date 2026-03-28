import folium
from folium.plugins import HeatMap
from .models import CrimeRecord


def generate_heatmap(crime_type_filter=None, area_filter=None):
    """Generate a standalone heatmap — optionally filtered."""
    crimes = CrimeRecord.objects.all()

    if crime_type_filter:
        crimes = crimes.filter(crime_type__icontains=crime_type_filter)
    if area_filter:
        crimes = crimes.filter(area__icontains=area_filter)

    m = folium.Map(location=[12.9716, 77.5946], zoom_start=12, tiles='CartoDB positron')

    heat_data = [
        [c.latitude, c.longitude]
        for c in crimes
        if c.latitude and c.longitude
    ]
    if heat_data:
        HeatMap(heat_data, radius=18, blur=15).add_to(m)

    return m._repr_html_(), crimes.count()
