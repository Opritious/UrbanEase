from rest_framework import serializers
from .models import (
    TransportRoute, TransportVehicle, ParkingSpot, EVChargingStation,
    TrafficData, UserTransportActivity
)


class TransportRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportRoute
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class TransportVehicleSerializer(serializers.ModelSerializer):
    route = TransportRouteSerializer(read_only=True)
    
    class Meta:
        model = TransportVehicle
        fields = '__all__'
        read_only_fields = ['last_updated']


class ParkingSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = '__all__'
        read_only_fields = ['last_updated']


class EVChargingStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EVChargingStation
        fields = '__all__'
        read_only_fields = ['last_updated']


class TrafficDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficData
        fields = '__all__'
        read_only_fields = ['timestamp']


class UserTransportActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTransportActivity
        fields = '__all__'
        read_only_fields = ['timestamp']


class RouteSearchSerializer(serializers.Serializer):
    start_location = serializers.JSONField()
    end_location = serializers.JSONField()
    preferred_mode = serializers.CharField(required=False)
    departure_time = serializers.DateTimeField(required=False)


class ParkingSearchSerializer(serializers.Serializer):
    location = serializers.JSONField()
    radius = serializers.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    spot_type = serializers.CharField(required=False)


class EVChargingSearchSerializer(serializers.Serializer):
    location = serializers.JSONField()
    radius = serializers.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    charger_type = serializers.CharField(required=False) 