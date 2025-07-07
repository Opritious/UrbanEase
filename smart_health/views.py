from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
from .models import (
    HealthProfile, HealthMetric, HealthAlert, TelemedicineAppointment,
    EmergencyService, EmergencyRequest, PollutionData
)
from .serializers import (
    HealthProfileSerializer, HealthMetricSerializer, HealthAlertSerializer,
    TelemedicineAppointmentSerializer, EmergencyServiceSerializer, EmergencyRequestSerializer,
    PollutionDataSerializer, HealthInsightSerializer, EmergencyRequestCreateSerializer
)


class HealthViewSet(viewsets.ModelViewSet):
    queryset = HealthProfile.objects.all()
    serializer_class = HealthProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HealthProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current user's health profile."""
        try:
            profile = request.user.health_profile
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except HealthProfile.DoesNotExist:
            return Response({'error': 'Health profile not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        """Update current user's health profile."""
        try:
            profile = request.user.health_profile
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except HealthProfile.DoesNotExist:
            return Response({'error': 'Health profile not found'}, status=status.HTTP_404_NOT_FOUND)


class HealthMetricViewSet(viewsets.ModelViewSet):
    queryset = HealthMetric.objects.all()
    serializer_class = HealthMetricSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HealthMetric.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def latest_metrics(self, request):
        """Get latest health metrics for current user."""
        metrics = self.get_queryset().order_by('-timestamp')[:10]
        serializer = self.get_serializer(metrics, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def metric_history(self, request):
        """Get metric history for a specific type."""
        metric_type = request.query_params.get('type')
        if metric_type:
            metrics = self.get_queryset().filter(metric_type=metric_type).order_by('-timestamp')[:50]
            serializer = self.get_serializer(metrics, many=True)
            return Response(serializer.data)
        return Response({'error': 'Metric type required'}, status=status.HTTP_400_BAD_REQUEST)


class HealthAlertViewSet(viewsets.ModelViewSet):
    queryset = HealthAlert.objects.all()
    serializer_class = HealthAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HealthAlert.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def active_alerts(self, request):
        """Get active health alerts for current user."""
        alerts = self.get_queryset().filter(is_resolved=False)
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def resolve_alert(self, request, pk=None):
        """Mark an alert as resolved."""
        alert = self.get_object()
        alert.is_resolved = True
        alert.resolved_at = timezone.now()
        alert.save()
        return Response({'message': 'Alert resolved successfully'})


class TelemedicineViewSet(viewsets.ModelViewSet):
    queryset = TelemedicineAppointment.objects.all()
    serializer_class = TelemedicineAppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TelemedicineAppointment.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def upcoming_appointments(self, request):
        """Get upcoming telemedicine appointments."""
        appointments = self.get_queryset().filter(
            appointment_date__gte=timezone.now(),
            status='scheduled'
        ).order_by('appointment_date')
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def join_meeting(self, request, pk=None):
        """Join a telemedicine meeting."""
        appointment = self.get_object()
        if appointment.status == 'scheduled':
            appointment.status = 'in_progress'
            appointment.save()
            return Response({
                'message': 'Meeting started',
                'meeting_link': appointment.meeting_link
            })
        return Response({'error': 'Meeting not available'}, status=status.HTTP_400_BAD_REQUEST)


class EmergencyViewSet(viewsets.ModelViewSet):
    queryset = EmergencyService.objects.all()
    serializer_class = EmergencyServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def available_services(self, request):
        """Get available emergency services."""
        services = EmergencyService.objects.filter(is_available=True)
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def request_emergency(self, request):
        """Request emergency service."""
        serializer = EmergencyRequestCreateSerializer(data=request.data)
        if serializer.is_valid():
            service_type = serializer.validated_data['service_type']
            location = serializer.validated_data['location']
            description = serializer.validated_data['description']
            priority = serializer.validated_data['priority']

            # Find available service
            service = EmergencyService.objects.filter(
                service_type=service_type,
                is_available=True
            ).first()

            if service:
                EmergencyRequest.objects.create(
                    user=request.user,
                    service=service,
                    location=location,
                    description=description,
                    priority=priority
                )
                return Response({'message': 'Emergency request sent successfully'})
            return Response({'error': 'No available service'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmergencyRequestViewSet(viewsets.ModelViewSet):
    queryset = EmergencyRequest.objects.all()
    serializer_class = EmergencyRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmergencyRequest.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def active_requests(self, request):
        """Get active emergency requests."""
        requests = self.get_queryset().exclude(status__in=['completed', 'cancelled'])
        serializer = self.get_serializer(requests, many=True)
        return Response(serializer.data)


class PollutionViewSet(viewsets.ModelViewSet):
    queryset = PollutionData.objects.all()
    serializer_class = PollutionDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def current_pollution(self, request):
        """Get current pollution data."""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        
        if lat and lng:
            # Mock pollution data for the location
            pollution_data = PollutionData.objects.filter(
                location__contains={'lat': float(lat), 'lng': float(lng)}
            ).first()
            
            if pollution_data:
                serializer = self.get_serializer(pollution_data)
                return Response(serializer.data)
            else:
                # Return mock data
                return Response({
                    'location': {'lat': float(lat), 'lng': float(lng)},
                    'air_quality_index': 45,
                    'pm25': 12.5,
                    'pm10': 25.0,
                    'ozone': 35.0,
                    'nitrogen_dioxide': 15.0,
                    'carbon_monoxide': 0.5,
                    'risk_level': 'good',
                    'timestamp': timezone.now()
                })
        return Response({'error': 'Location parameters required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def health_insights(self, request):
        """Get AI-based health insights based on pollution data."""
        # Mock AI insights
        insights = [
            {
                'insight_type': 'pollution_risk',
                'message': 'Air quality is good. Safe for outdoor activities.',
                'severity': 'low',
                'recommendations': [
                    'Continue outdoor activities',
                    'Consider walking or cycling for short trips'
                ],
                'timestamp': timezone.now()
            }
        ]
        serializer = HealthInsightSerializer(insights, many=True)
        return Response(serializer.data) 