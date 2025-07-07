from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# User Management
from user_management.models import UserProfile, UserActivity

# Smart Mobility
from smart_mobility.models import (
    TransportRoute, TransportVehicle, ParkingSpot, EVChargingStation,
    TrafficData, UserTransportActivity
)

# Smart Health
from smart_health.models import (
    HealthProfile, HealthMetric, HealthAlert, TelemedicineAppointment,
    EmergencyService, EmergencyRequest, PollutionData
)

# Smart Safety
from smart_safety.models import (
    DisasterAlert, SafetyZone, FraudDetection, SecurityIncident,
    SafetyCheck, EmergencyContact, SafetyNotification
)


# User Management Admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'emergency_contact', 'created_at']
    list_filter = ['city', 'created_at']
    search_fields = ['user__username', 'user__email', 'city']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'location', 'timestamp']
    list_filter = ['activity_type', 'timestamp']
    search_fields = ['user__username', 'activity_type']


# Smart Mobility Admin
@admin.register(TransportRoute)
class TransportRouteAdmin(admin.ModelAdmin):
    list_display = ['route_id', 'route_name', 'route_type', 'is_active', 'created_at']
    list_filter = ['route_type', 'is_active', 'created_at']
    search_fields = ['route_id', 'route_name']


@admin.register(TransportVehicle)
class TransportVehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_id', 'route', 'status', 'occupancy', 'last_updated']
    list_filter = ['status', 'route__route_type', 'last_updated']
    search_fields = ['vehicle_id', 'route__route_name']


@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ['spot_id', 'spot_type', 'is_available', 'hourly_rate', 'zone']
    list_filter = ['spot_type', 'is_available', 'zone']
    search_fields = ['spot_id', 'zone']


@admin.register(EVChargingStation)
class EVChargingStationAdmin(admin.ModelAdmin):
    list_display = ['station_id', 'station_name', 'charger_type', 'is_available', 'current_user']
    list_filter = ['charger_type', 'is_available', 'last_updated']
    search_fields = ['station_id', 'station_name']


@admin.register(TrafficData)
class TrafficDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'traffic_level', 'average_speed', 'congestion_index', 'timestamp']
    list_filter = ['traffic_level', 'incident_reported', 'timestamp']
    search_fields = ['location']


@admin.register(UserTransportActivity)
class UserTransportActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'distance', 'duration', 'carbon_saved', 'timestamp']
    list_filter = ['activity_type', 'timestamp']
    search_fields = ['user__username', 'activity_type']


# Smart Health Admin
@admin.register(HealthProfile)
class HealthProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'blood_type', 'emergency_contact', 'created_at']
    list_filter = ['blood_type', 'created_at']
    search_fields = ['user__username', 'emergency_contact']


@admin.register(HealthMetric)
class HealthMetricAdmin(admin.ModelAdmin):
    list_display = ['user', 'metric_type', 'value', 'unit', 'timestamp']
    list_filter = ['metric_type', 'timestamp']
    search_fields = ['user__username', 'metric_type']


@admin.register(HealthAlert)
class HealthAlertAdmin(admin.ModelAdmin):
    list_display = ['user', 'alert_type', 'severity', 'is_resolved', 'created_at']
    list_filter = ['alert_type', 'severity', 'is_resolved', 'created_at']
    search_fields = ['user__username', 'alert_type']


@admin.register(TelemedicineAppointment)
class TelemedicineAppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'doctor_name', 'doctor_specialty', 'appointment_date', 'status']
    list_filter = ['status', 'doctor_specialty', 'appointment_date']
    search_fields = ['user__username', 'doctor_name']


@admin.register(EmergencyService)
class EmergencyServiceAdmin(admin.ModelAdmin):
    list_display = ['service_id', 'service_type', 'is_available', 'current_user', 'status']
    list_filter = ['service_type', 'is_available', 'status']
    search_fields = ['service_id', 'service_type']


@admin.register(EmergencyRequest)
class EmergencyRequestAdmin(admin.ModelAdmin):
    list_display = ['request_id', 'user', 'service', 'priority', 'status', 'created_at']
    list_filter = ['priority', 'status', 'created_at']
    search_fields = ['request_id', 'user__username']


@admin.register(PollutionData)
class PollutionDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'air_quality_index', 'risk_level', 'timestamp']
    list_filter = ['risk_level', 'timestamp']
    search_fields = ['location']


# Smart Safety Admin
@admin.register(DisasterAlert)
class DisasterAlertAdmin(admin.ModelAdmin):
    list_display = ['alert_id', 'disaster_type', 'severity', 'is_active', 'created_at']
    list_filter = ['disaster_type', 'severity', 'is_active', 'created_at']
    search_fields = ['alert_id', 'disaster_type']


@admin.register(SafetyZone)
class SafetyZoneAdmin(admin.ModelAdmin):
    list_display = ['zone_id', 'zone_name', 'zone_type', 'is_available', 'capacity', 'current_occupancy']
    list_filter = ['zone_type', 'is_available', 'created_at']
    search_fields = ['zone_id', 'zone_name']


@admin.register(FraudDetection)
class FraudDetectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'fraud_type', 'risk_score', 'is_blocked', 'is_resolved', 'created_at']
    list_filter = ['fraud_type', 'is_blocked', 'is_resolved', 'created_at']
    search_fields = ['user__username', 'fraud_type']


@admin.register(SecurityIncident)
class SecurityIncidentAdmin(admin.ModelAdmin):
    list_display = ['incident_id', 'user', 'incident_type', 'severity', 'status', 'created_at']
    list_filter = ['incident_type', 'severity', 'status', 'created_at']
    search_fields = ['incident_id', 'user__username']


@admin.register(SafetyCheck)
class SafetyCheckAdmin(admin.ModelAdmin):
    list_display = ['user', 'check_type', 'status', 'is_automated', 'created_at']
    list_filter = ['check_type', 'status', 'is_automated', 'created_at']
    search_fields = ['user__username', 'check_type']


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'relationship', 'phone_number', 'is_primary']
    list_filter = ['relationship', 'is_primary', 'created_at']
    search_fields = ['user__username', 'name']


@admin.register(SafetyNotification)
class SafetyNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'priority', 'is_read', 'created_at']
    list_filter = ['notification_type', 'priority', 'is_read', 'created_at']
    search_fields = ['user__username', 'title']


# User Profile Inline
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'


# Custom User Admin
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email']


# Re-register User model
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin) 