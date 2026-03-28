import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forecast import get_crime_forecast, get_monthly_trend, get_crime_type_distribution


@login_required
def forecast_dashboard(request):
    forecast_data = get_crime_forecast()
    monthly_trend = get_monthly_trend()
    type_dist = get_crime_type_distribution()

    if forecast_data:
        bar_labels = json.dumps([item['area'] for item in forecast_data])
        bar_historical = json.dumps([item['historical'] for item in forecast_data])
        bar_predicted = json.dumps([item['predicted'] for item in forecast_data])
    else:
        # Fallback demo data when DB is empty
        bar_labels = json.dumps(['Central', 'Market', 'Station', 'Airport', 'Koramangala'])
        bar_historical = json.dumps([38, 52, 29, 18, 43])
        bar_predicted = json.dumps([42, 57, 32, 20, 47])

    return render(request, 'crime_forecast/forecast.html', {
        'forecast_data': forecast_data,
        'bar_labels': bar_labels,
        'bar_historical': bar_historical,
        'bar_predicted': bar_predicted,
        'trend_labels': json.dumps(monthly_trend['labels']),
        'trend_values': json.dumps(monthly_trend['values']),
        'type_labels': json.dumps(type_dist['labels']),
        'type_values': json.dumps(type_dist['values']),
        'record_count': sum(item['historical'] for item in forecast_data),
    })
