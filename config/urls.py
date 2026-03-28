from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="landing/landing.html"), name='landing'),
    path('dashboard/', include('apps.dashboard.urls')),
    path('hotspots/', include('apps.crime_hotspot.urls')),
    path('forecast/', include('apps.crime_forecast.urls')),
    path('classifier/', include('apps.nlp_classifier.urls')),
    path('route/', include('apps.safe_route.urls')),
    path('sos/', include('apps.sos_system.urls')),          # ← was missing
    path('accounts/', include('apps.accounts.urls')),
    path('api/', include('api.urls')),                      # ← REST API
]
