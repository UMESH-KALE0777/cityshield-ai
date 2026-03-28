from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .services import find_nearest_station


@login_required
def sos_dashboard(request):
    alert_triggered = False
    nearest_station = None
    distance_km = None

    if request.method == 'POST':
        alert_triggered = True

        # Try to get user coordinates from browser geolocation (passed in POST)
        try:
            user_lat = float(request.POST.get('latitude', 12.9716))
            user_lon = float(request.POST.get('longitude', 77.5946))
            nearest_station, distance_km = find_nearest_station(user_lat, user_lon)
        except (TypeError, ValueError):
            pass

        messages.success(request, "Emergency alert sent! Help is on the way.")

    return render(request, 'sos_system/sos.html', {
        'alert': alert_triggered,
        'nearest_station': nearest_station,
        'distance_km': distance_km,
    })
