from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
from .models import (
    DisasterAlert, SafetyZone, FraudDetection, SecurityIncident,
    SafetyCheck, EmergencyContact, SafetyNotification
)
from .serializers import (
    DisasterAlertSerializer, SafetyZoneSerializer, FraudDetectionSerializer,
    SecurityIncidentSerializer, SafetyCheckSerializer, EmergencyContactSerializer,
    SafetyNotificationSerializer, DisasterAlertCreateSerializer,
    SecurityIncidentCreateSerializer, SafetyCheckCreateSerializer
)
from .services import weather_service
from rest_framework.permissions import AllowAny


class SafetyViewSet(viewsets.ModelViewSet):
    queryset = DisasterAlert.objects.all()
    serializer_class = DisasterAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def active_alerts(self, request):
        """Get active disaster alerts."""
        alerts = DisasterAlert.objects.filter(is_active=True)
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def nearby_alerts(self, request):
        """Get disaster alerts near user's location."""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        
        if lat and lng:
            # Mock nearby alerts logic
            alerts = DisasterAlert.objects.filter(is_active=True)[:5]
            serializer = self.get_serializer(alerts, many=True)
            return Response(serializer.data)
        return Response({'error': 'Location parameters required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_alert(self, request):
        """Create a new disaster alert (admin only)."""
        serializer = DisasterAlertCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Mock alert creation
            return Response({'message': 'Alert created successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SafetyZoneViewSet(viewsets.ModelViewSet):
    queryset = SafetyZone.objects.all()
    serializer_class = SafetyZoneSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def nearby_zones(self, request):
        """Get safety zones near user's location."""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        
        if lat and lng:
            # Mock nearby zones logic
            zones = SafetyZone.objects.filter(is_available=True)[:10]
            serializer = self.get_serializer(zones, many=True)
            return Response(serializer.data)
        return Response({'error': 'Location parameters required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def evacuation_centers(self, request):
        """Get evacuation centers."""
        centers = SafetyZone.objects.filter(zone_type='evacuation_center', is_available=True)
        serializer = self.get_serializer(centers, many=True)
        return Response(serializer.data)


class FraudDetectionViewSet(viewsets.ModelViewSet):
    queryset = FraudDetection.objects.all()
    serializer_class = FraudDetectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FraudDetection.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def active_detections(self, request):
        """Get active fraud detections for current user."""
        detections = self.get_queryset().filter(is_resolved=False)
        serializer = self.get_serializer(detections, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def resolve_detection(self, request, pk=None):
        """Mark a fraud detection as resolved."""
        detection = self.get_object()
        detection.is_resolved = True
        detection.resolved_at = timezone.now()
        detection.save()
        return Response({'message': 'Fraud detection resolved successfully'})

    @action(detail=False, methods=['get'])
    def risk_summary(self, request):
        """Get fraud risk summary for current user."""
        from django.db import models
        detections = self.get_queryset()
        total_detections = detections.count()
        active_detections = detections.filter(is_resolved=False).count()
        avg_risk_score = detections.aggregate(avg_risk=models.Avg('risk_score'))['avg_risk_score'] or 0
        
        return Response({
            'total_detections': total_detections,
            'active_detections': active_detections,
            'average_risk_score': avg_risk_score,
            'risk_level': 'high' if avg_risk_score > 0.7 else 'medium' if avg_risk_score > 0.3 else 'low'
        })


class SecurityIncidentViewSet(viewsets.ModelViewSet):
    queryset = SecurityIncident.objects.all()
    serializer_class = SecurityIncidentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SecurityIncident.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def report_incident(self, request):
        """Report a security incident."""
        serializer = SecurityIncidentCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Mock incident creation
            return Response({'message': 'Security incident reported successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def recent_incidents(self, request):
        """Get recent security incidents for current user."""
        incidents = self.get_queryset().order_by('-created_at')[:10]
        serializer = self.get_serializer(incidents, many=True)
        return Response(serializer.data)


class SafetyCheckViewSet(viewsets.ModelViewSet):
    queryset = SafetyCheck.objects.all()
    serializer_class = SafetyCheckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SafetyCheck.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def check_in(self, request):
        """Perform a safety check-in."""
        serializer = SafetyCheckCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Mock check-in creation
            return Response({'message': 'Safety check-in completed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def check_history(self, request):
        """Get safety check history for current user."""
        checks = self.get_queryset().order_by('-created_at')[:20]
        serializer = self.get_serializer(checks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def automated_check(self, request):
        """Perform automated safety check."""
        # Mock automated check
        return Response({
            'status': 'safe',
            'message': 'Automated safety check completed',
            'location': {'lat': 0, 'lng': 0},
            'timestamp': timezone.now()
        })


class EmergencyContactViewSet(viewsets.ModelViewSet):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def primary_contact(self, request):
        """Get primary emergency contact for current user."""
        contact = self.get_queryset().filter(is_primary=True).first()
        if contact:
            serializer = self.get_serializer(contact)
            return Response(serializer.data)
        return Response({'error': 'No primary contact found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def notify_contacts(self, request):
        """Notify emergency contacts."""
        message = request.data.get('message')
        if message:
            # Mock notification logic
            return Response({'message': 'Emergency contacts notified successfully'})
        return Response({'error': 'Message required'}, status=status.HTTP_400_BAD_REQUEST)


class SafetyNotificationViewSet(viewsets.ModelViewSet):
    queryset = SafetyNotification.objects.all()
    serializer_class = SafetyNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SafetyNotification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def unread_notifications(self, request):
        """Get unread safety notifications for current user."""
        notifications = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a notification as read."""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read."""
        self.get_queryset().update(is_read=True)
        return Response({'message': 'All notifications marked as read'})


@api_view(['GET'])
@permission_classes([AllowAny])
def weather_current(request):
    """Get current weather for Kolkata"""
    try:
        weather_data = weather_service.get_current_weather()
        return Response({
            'success': True,
            'data': weather_data
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def weather_forecast(request):
    """Get weather forecast for Kolkata"""
    try:
        forecast_data = weather_service.get_weather_forecast()
        return Response({
            'success': True,
            'data': forecast_data
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def weather_alerts(request):
    """Get weather alerts for Kolkata"""
    try:
        alerts_data = weather_service.get_weather_alerts()
        return Response({
            'success': True,
            'data': alerts_data
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 