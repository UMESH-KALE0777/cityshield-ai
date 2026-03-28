from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
import json
from apps.crime_hotspot.models import CrimeRecord


# Bangalore area coordinates — used to build a rough map link
AREA_COORDS = {
    'central': (12.9716, 77.5946),
    'koramangala': (12.9352, 77.6245),
    'whitefield': (12.9698, 77.7499),
    'electronic city': (12.8399, 77.6770),
    'mg road': (12.9757, 77.6011),
    'indiranagar': (12.9784, 77.6408),
    'jayanagar': (12.9250, 77.5938),
    'rajajinagar': (12.9849, 77.5521),
    'hebbal': (13.0351, 77.5970),
    'yelahanka': (13.1007, 77.5963),
}


def get_area_safety(area_name: str) -> dict:
    """
    Compute safety index (0-100) for a given area string.
    Matches CrimeRecord.area with a case-insensitive contains lookup.
    """
    crime_count = CrimeRecord.objects.filter(
        area__icontains=area_name
    ).count()

    # Scale: 0 crimes → 100 (safest), 50+ → 0 (most dangerous)
    raw_score = max(0, 100 - (crime_count * 2))

    if raw_score >= 70:
        risk_level = 'Low'
        risk_color = 'green'
        advice = 'This area has low recorded crime. Normal precautions apply.'
    elif raw_score >= 40:
        risk_level = 'Medium'
        risk_color = 'yellow'
        advice = 'Moderate crime levels. Stay alert, avoid isolated spots at night.'
    else:
        risk_level = 'High'
        risk_color = 'red'
        advice = 'High crime area. Travel in groups, avoid late-night travel if possible.'

    return {
        'score': raw_score,
        'crime_count': crime_count,
        'risk_level': risk_level,
        'risk_color': risk_color,
        'advice': advice,
    }


def get_map_link(source: str, destination: str) -> str:
    """Return a Google Maps directions URL for the source → destination pair."""
    base = "https://www.google.com/maps/dir/"
    src_encoded = source.replace(' ', '+') + '+Bangalore'
    dst_encoded = destination.replace(' ', '+') + '+Bangalore'
    return f"{base}{src_encoded}/{dst_encoded}"


@login_required
def route_dashboard(request):

    area_counts = (
        CrimeRecord.objects
        .values('area')
        .annotate(count=Count('id'))
        .order_by('-count')[:60]
    )

    crime_by_area = {
        row['area']: row['count']
        for row in area_counts
    }

    route = None

    if request.method == 'POST':

        source = request.POST.get(
            'source', ''
        ).strip()

        destination = request.POST.get(
            'destination', ''
        ).strip()

        if source and destination:

            src_info = get_area_safety(source)

            dst_info = get_area_safety(destination)

            overall = round(
                (src_info['score']
                 + dst_info['score']) / 2
            )

            route = {

                'source': source,

                'destination': destination,

                'overall_score': overall,

                'overall_risk':

                    'High'
                    if overall < 40
                    else 'Medium'
                    if overall < 70
                    else 'Low',

                'map_link':
                    get_map_link(
                        source,
                        destination
                    )

            }

    return render(

        request,

        'safe_route/route.html',

        {

            'route': route,

            'crime_by_area':
                json.dumps(crime_by_area)

        }
    )
