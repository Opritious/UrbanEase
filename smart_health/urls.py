from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HealthViewSet, HealthMetricViewSet, HealthAlertViewSet,
    TelemedicineViewSet, EmergencyViewSet, EmergencyRequestViewSet,
    PollutionViewSet
)

router = DefaultRouter()
router.register(r'profiles', HealthViewSet, basename='health-profile')
router.register(r'metrics', HealthMetricViewSet, basename='health-metrics')
router.register(r'alerts', HealthAlertViewSet, basename='health-alerts')
router.register(r'telemedicine', TelemedicineViewSet, basename='telemedicine')
router.register(r'emergency', EmergencyViewSet)
router.register(r'emergency-requests', EmergencyRequestViewSet, basename='emergency-requests')
router.register(r'pollution', PollutionViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 