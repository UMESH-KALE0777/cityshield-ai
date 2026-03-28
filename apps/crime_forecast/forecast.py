from collections import Counter, defaultdict
from datetime import date, timedelta
from apps.crime_hotspot.models import CrimeRecord


def get_crime_forecast():
    """
    Returns top-10 areas by crime count with a simple naive forecast
    (historical average + 10% uplift as predicted next-period value).
    """
    crimes = CrimeRecord.objects.all()
    if not crimes.exists():
        return []

    area_counts = Counter(c.area for c in crimes)

    # Total crimes for percentage calculation
    total = sum(area_counts.values())

    forecast_data = []
    for area, count in area_counts.most_common(10):
        # Naive forecast: historical count * 1.10 (10% trend uplift)
        predicted = round(count * 1.10)
        pct = round((count / total) * 100, 1) if total else 0
        forecast_data.append({
            'area': area,
            'historical': count,
            'predicted': predicted,
            'percentage': pct,
        })

    return forecast_data


def get_monthly_trend():
    """
    Returns crime counts grouped by month (last 12 months).
    Used for the trend line chart.
    """
    today = date.today()
    twelve_months_ago = today - timedelta(days=365)

    crimes = CrimeRecord.objects.filter(
        date__gte=twelve_months_ago,
        date__isnull=False,
    )

    monthly = defaultdict(int)
    for crime in crimes:
        key = crime.date.strftime('%b %Y')
        monthly[key] += 1

    # Return sorted by date
    sorted_months = sorted(monthly.items(), key=lambda x: x[0])
    return {
        'labels': [m[0] for m in sorted_months],
        'values': [m[1] for m in sorted_months],
    }


def get_crime_type_distribution():
    """Returns crime counts by type for a donut/pie chart."""
    crimes = CrimeRecord.objects.all()
    type_counts = Counter(c.crime_type for c in crimes)
    return {
        'labels': list(type_counts.keys()),
        'values': list(type_counts.values()),
    }
