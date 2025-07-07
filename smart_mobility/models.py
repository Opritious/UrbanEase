from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class TransportRoute(models.Model):
    """Public transport routes and schedules."""
    ROUTE_TYPES = [
        ('bus', 'Bus'),
        ('metro', 'Metro'),
        ('train', 'Train'),
        ('tram', 'Tram'),
        ('bike', 'Bike Share'),
    ]
    
    route_id = models.CharField(max_length=50, unique=True)
    route_name = models.CharField(max_length=200)
    route_type = models.CharField(max_length=20, choices=ROUTE_TYPES)
    start_station = models.CharField(max_length=200)
    end_station = models.CharField(max_length=200)
    stops = models.JSONField()  # List of stops with coordinates
    schedule = models.JSONField()  # Schedule data
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.route_name} ({self.route_type})"


class TransportVehicle(models.Model):
    """Individual vehicles for real-time tracking."""
    vehicle_id = models.CharField(max_length=50, unique=True)
    route = models.ForeignKey(TransportRoute, on_delete=models.CASCADE, related_name='vehicles')
    current_location = models.JSONField()  # {lat: float, lng: float}
    speed = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # km/h
    capacity = models.IntegerField(default=0)
    occupancy = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('maintenance', 'Maintenance'),
        ('inactive', 'Inactive'),
    ], default='active')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Vehicle {self.vehicle_id} on {self.route.route_name}"


class ParkingSpot(models.Model):
    """Smart parking spots with real-time availability."""
    spot_id = models.CharField(max_length=50, unique=True)
    location = models.JSONField()  # {lat: float, lng: float}
    spot_type = models.CharField(max_length=20, choices=[
        ('standard', 'Standard'),
        ('disabled', 'Disabled'),
        ('electric', 'Electric Vehicle'),
        ('bike', 'Bike'),
    ])
    is_available = models.BooleanField(default=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    zone = models.CharField(max_length=50, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Parking Spot {self.spot_id} ({self.spot_type})"


class EVChargingStation(models.Model):
    """Electric vehicle charging stations."""
    station_id = models.CharField(max_length=50, unique=True)
    location = models.JSONField()  # {lat: float, lng: float}
    station_name = models.CharField(max_length=200)
    charger_type = models.CharField(max_length=20, choices=[
        ('slow', 'Slow Charger'),
        ('fast', 'Fast Charger'),
        ('super', 'Super Charger'),
    ])
    is_available = models.BooleanField(default=True)
    current_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    charging_rate = models.DecimalField(max_digits=5, decimal_places=2)  # kW
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"EV Station {self.station_id} ({self.charger_type})"


class TrafficData(models.Model):
    """AI-based traffic management data."""
    location = models.JSONField()  # {lat: float, lng: float}
    traffic_level = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('severe', 'Severe'),
    ])
    average_speed = models.DecimalField(max_digits=5, decimal_places=2)  # km/h
    congestion_index = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1)])
    incident_reported = models.BooleanField(default=False)
    incident_description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Traffic at {self.location} - {self.traffic_level}"


class UserTransportActivity(models.Model):
    """Track user transport activities for analytics."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transport_activities')
    activity_type = models.CharField(max_length=20, choices=[
        ('bus', 'Bus'),
        ('metro', 'Metro'),
        ('train', 'Train'),
        ('bike', 'Bike'),
        ('walking', 'Walking'),
        ('car', 'Car'),
        ('ev', 'Electric Vehicle'),
    ])
    start_location = models.JSONField()
    end_location = models.JSONField()
    distance = models.DecimalField(max_digits=8, decimal_places=2)  # km
    duration = models.IntegerField()  # minutes
    carbon_saved = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # kg CO2
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} trip" 