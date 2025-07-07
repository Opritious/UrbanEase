from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    SafetyViewSet, SafetyZoneViewSet, FraudDetectionViewSet,
    SecurityIncidentViewSet, SafetyCheckViewSet, EmergencyContactViewSet,
    SafetyNotificationViewSet
)

router = DefaultRouter()
router.register(r'alerts', SafetyViewSet)
router.register(r'zones', SafetyZoneViewSet)
router.register(r'fraud', FraudDetectionViewSet, basename='fraud-detection')
router.register(r'incidents', SecurityIncidentViewSet, basename='security-incidents')
router.register(r'checks', SafetyCheckViewSet, basename='safety-checks')
router.register(r'contacts', EmergencyContactViewSet, basename='emergency-contacts')
router.register(r'notifications', SafetyNotificationViewSet, basename='safety-notifications')

urlpatterns = [
    path('', include(router.urls)),
    path('weather/current/', views.weather_current, name='weather_current'),
    path('weather/forecast/', views.weather_forecast, name='weather_forecast'),
    path('weather/alerts/', views.weather_alerts, name='weather_alerts'),
] 