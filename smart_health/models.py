from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class HealthProfile(models.Model):
    """Extended health profile for users."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_profile')
    blood_type = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    insurance_provider = models.CharField(max_length=100, blank=True)
    insurance_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Health Profile"


class HealthMetric(models.Model):
    """Health metrics tracking."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_metrics')
    metric_type = models.CharField(max_length=50, choices=[
        ('heart_rate', 'Heart Rate'),
        ('blood_pressure', 'Blood Pressure'),
        ('temperature', 'Temperature'),
        ('oxygen_saturation', 'Oxygen Saturation'),
        ('steps', 'Steps'),
        ('sleep_hours', 'Sleep Hours'),
        ('weight', 'Weight'),
        ('bmi', 'BMI'),
    ])
    value = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.metric_type}: {self.value} {self.unit}"


class HealthAlert(models.Model):
    """AI-based health risk alerts."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_alerts')
    alert_type = models.CharField(max_length=50, choices=[
        ('high_heart_rate', 'High Heart Rate'),
        ('low_oxygen', 'Low Oxygen Saturation'),
        ('high_temperature', 'High Temperature'),
        ('irregular_pattern', 'Irregular Pattern'),
        ('pollution_risk', 'Pollution Risk'),
        ('allergy_alert', 'Allergy Alert'),
    ])
    severity = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ])
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.alert_type} ({self.severity})"


class TelemedicineAppointment(models.Model):
    """Telemedicine appointments."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='telemedicine_appointments')
    doctor_name = models.CharField(max_length=100)
    doctor_specialty = models.CharField(max_length=100)
    appointment_date = models.DateTimeField()
    duration = models.IntegerField(default=30)  # minutes
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='scheduled')
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['appointment_date']

    def __str__(self):
        return f"{self.user.username} - {self.doctor_name} on {self.appointment_date}"


class EmergencyService(models.Model):
    """GPS-enabled emergency services."""
    service_id = models.CharField(max_length=50, unique=True)
    service_type = models.CharField(max_length=50, choices=[
        ('ambulance', 'Ambulance'),
        ('fire', 'Fire Department'),
        ('police', 'Police'),
        ('rescue', 'Rescue'),
    ])
    location = models.JSONField()  # {lat: float, lng: float}
    is_available = models.BooleanField(default=True)
    current_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    estimated_arrival = models.IntegerField(null=True, blank=True)  # minutes
    status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('dispatched', 'Dispatched'),
        ('on_way', 'On Way'),
        ('arrived', 'Arrived'),
        ('completed', 'Completed'),
    ], default='available')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service_type} {self.service_id}"


class EmergencyRequest(models.Model):
    """Emergency service requests."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_requests')
    service = models.ForeignKey(EmergencyService, on_delete=models.CASCADE, related_name='requests')
    location = models.JSONField()
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], default='medium')
    status = models.CharField(max_length=20, choices=[
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='requested')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Emergency request by {self.user.username} - {self.status}"


class PollutionData(models.Model):
    """Air pollution monitoring data."""
    location = models.JSONField()  # {lat: float, lng: float}
    air_quality_index = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(500)])
    pm25 = models.DecimalField(max_digits=5, decimal_places=2)  # μg/m³
    pm10 = models.DecimalField(max_digits=5, decimal_places=2)  # μg/m³
    ozone = models.DecimalField(max_digits=5, decimal_places=2)  # ppb
    nitrogen_dioxide = models.DecimalField(max_digits=5, decimal_places=2)  # ppb
    carbon_monoxide = models.DecimalField(max_digits=5, decimal_places=2)  # ppm
    risk_level = models.CharField(max_length=20, choices=[
        ('good', 'Good'),
        ('moderate', 'Moderate'),
        ('unhealthy_sensitive', 'Unhealthy for Sensitive Groups'),
        ('unhealthy', 'Unhealthy'),
        ('very_unhealthy', 'Very Unhealthy'),
        ('hazardous', 'Hazardous'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Pollution at {self.location} - AQI: {self.air_quality_index}" 