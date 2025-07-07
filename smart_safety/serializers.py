from rest_framework import serializers
from .models import (
    DisasterAlert, SafetyZone, FraudDetection, SecurityIncident,
    SafetyCheck, EmergencyContact, SafetyNotification
)


class DisasterAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisasterAlert
        fields = '__all__'
        read_only_fields = ['created_at']


class SafetyZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyZone
        fields = '__all__'
        read_only_fields = ['created_at']


class FraudDetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraudDetection
        fields = '__all__'
        read_only_fields = ['created_at', 'resolved_at']


class SecurityIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityIncident
        fields = '__all__'
        read_only_fields = ['created_at', 'resolved_at']


class SafetyCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyCheck
        fields = '__all__'
        read_only_fields = ['created_at']


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'
        read_only_fields = ['created_at']


class SafetyNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyNotification
        fields = '__all__'
        read_only_fields = ['created_at']


class DisasterAlertCreateSerializer(serializers.Serializer):
    """Serializer for creating disaster alerts."""
    disaster_type = serializers.CharField()
    severity = serializers.CharField()
    location = serializers.JSONField()
    affected_area = serializers.JSONField()
    description = serializers.CharField()
    instructions = serializers.CharField()


class SecurityIncidentCreateSerializer(serializers.Serializer):
    """Serializer for creating security incidents."""
    incident_type = serializers.CharField()
    location = serializers.JSONField()
    description = serializers.CharField()
    severity = serializers.CharField(default='medium')
    evidence = serializers.ListField(child=serializers.CharField(), required=False)


class SafetyCheckCreateSerializer(serializers.Serializer):
    """Serializer for creating safety checks."""
    check_type = serializers.CharField()
    location = serializers.JSONField()
    status = serializers.CharField()
    message = serializers.CharField(required=False) 