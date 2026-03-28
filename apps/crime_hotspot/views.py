import folium
import random
from folium.plugins import HeatMap, MarkerCluster
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import CrimeRecord, CrimeReport
from .forms import CrimeReportForm


def jitter(val, amount=0.005):
    """Add tiny random offset so stacked points spread out on heatmap."""
    return val + random.uniform(-amount, amount)


@login_required
def hotspot_dashboard(request):
    crimes = CrimeRecord.objects.all()
    total = crimes.count()

    type_counts = (
        crimes.values('crime_type')
        .annotate(count=Count('crime_type'))
        .order_by('-count')[:8]
    )

    m = folium.Map(
        location=[12.9716, 77.5946],
        zoom_start=11,
        tiles='CartoDB positron',
    )

    # Heatmap with jitter to break up stacked coordinates
    heat_data = []
    for c in crimes:
        if c.latitude and c.longitude:
            heat_data.append([jitter(c.latitude), jitter(c.longitude)])

    if heat_data:
        HeatMap(
            heat_data,
            radius=12,
            blur=18,
            max_zoom=14,
            min_opacity=0.3,
            gradient={0.2: '#4575b4', 0.4: '#74add1', 0.6: '#fee090', 0.8: '#f46d43', 1.0: '#d73027'},
        ).add_to(m)

    # Clustered markers for first 300
    cluster = MarkerCluster(name="Incidents").add_to(m)
    color_map = {
        'Theft': 'orange', 'Robbery': 'red', 'Assault': 'darkred',
        'Kidnapping': 'purple', 'Murder': 'black', 'Cheating': 'blue',
        'Fraud': 'blue', 'Burglary': 'orange', 'Vandalism': 'gray',
        'Domestic Violence': 'darkred', 'Firearm Offense': 'black',
    }
    for crime in crimes.filter(latitude__isnull=False)[:300]:
        folium.CircleMarker(
            location=[crime.latitude, crime.longitude],
            radius=5,
            color=color_map.get(crime.crime_type, 'gray'),
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(
                f"<b>{crime.crime_type}</b><br>{crime.area}<br>{crime.date or ''}",
                max_width=180,
            ),
        ).add_to(cluster)

    folium.LayerControl().add_to(m)
    map_html = m._repr_html_()

    return render(request, 'crime_hotspot/hotspot_map.html', {
        'map': map_html,
        'total_crimes': total,
        'type_counts': type_counts,
    })


@login_required
def report_crime(request):
    if request.method == 'POST':
        form = CrimeReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Report submitted successfully.")
            return redirect('hotspot_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CrimeReportForm()
    return render(request, 'crime_hotspot/report.html', {'form': form})
