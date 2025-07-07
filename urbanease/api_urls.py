"""
Main API URL configuration for UrbanEase project.
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from user_management.views import UserViewSet
from smart_mobility.views import TransportViewSet, ParkingViewSet
from smart_health.views import HealthViewSet, EmergencyViewSet
from smart_safety.views import SafetyViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'transport', TransportViewSet)
router.register(r'parking', ParkingViewSet)
router.register(r'health', HealthViewSet)
router.register(r'emergency', EmergencyViewSet)
router.register(r'safety', SafetyViewSet)

urlpatterns = router.urls 