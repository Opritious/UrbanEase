from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TransportViewSet, ParkingViewSet, EVChargingViewSet,
    TrafficViewSet, UserTransportActivityViewSet
)

router = DefaultRouter()
router.register(r'routes', TransportViewSet)
router.register(r'parking', ParkingViewSet)
router.register(r'ev-charging', EVChargingViewSet)
router.register(r'traffic', TrafficViewSet)
router.register(r'activities', UserTransportActivityViewSet, basename='transport-activities')

urlpatterns = [
    path('', include(router.urls)),
] 