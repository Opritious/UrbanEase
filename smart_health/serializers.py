from rest_framework import serializers
from .models import (
    HealthProfile, HealthMetric, HealthAlert, TelemedicineAppointment,
    EmergencyService, EmergencyRequest, PollutionData
)


class HealthProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProfile
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class HealthMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthMetric
        fields = '__all__'
        read_only_fields = ['timestamp']


class HealthAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthAlert
        fields = '__all__'
        read_only_fields = ['created_at', 'resolved_at']


class TelemedicineAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemedicineAppointment
        fields = '__all__'
        read_only_fields = ['created_at']


class EmergencyServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyService
        fields = '__all__'
        read_only_fields = ['last_updated']


class EmergencyRequestSerializer(serializers.ModelSerializer):
    service = EmergencyServiceSerializer(read_only=True)
    
    class Meta:
        model = EmergencyRequest
        fields = '__all__'
        read_only_fields = ['created_at', 'completed_at']


class PollutionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollutionData
        fields = '__all__'
        read_only_fields = ['timestamp']


class HealthInsightSerializer(serializers.Serializer):
    """Serializer for AI-based health insights."""
    insight_type = serializers.CharField()
    message = serializers.CharField()
    severity = serializers.CharField()
    recommendations = serializers.ListField(child=serializers.CharField())
    timestamp = serializers.DateTimeField()


class EmergencyRequestCreateSerializer(serializers.Serializer):
    """Serializer for creating emergency requests."""
    service_type = serializers.CharField()
    location = serializers.JSONField()
    description = serializers.CharField()
    priority = serializers.CharField(default='medium') 