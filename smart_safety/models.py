from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class DisasterAlert(models.Model):
    """Disaster alert system."""
    alert_id = models.CharField(max_length=50, unique=True)
    disaster_type = models.CharField(max_length=50, choices=[
        ('earthquake', 'Earthquake'),
        ('flood', 'Flood'),
        ('fire', 'Fire'),
        ('storm', 'Storm'),
        ('tsunami', 'Tsunami'),
        ('volcanic_eruption', 'Volcanic Eruption'),
        ('terrorist_attack', 'Terrorist Attack'),
        ('chemical_spill', 'Chemical Spill'),
        ('other', 'Other'),
    ])
    severity = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ])
    location = models.JSONField()  # {lat: float, lng: float}
    affected_area = models.JSONField()  # Polygon or radius
    description = models.TextField()
    instructions = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.disaster_type} Alert - {self.severity}"


class SafetyZone(models.Model):
    """Safe zones and evacuation centers."""
    zone_id = models.CharField(max_length=50, unique=True)
    zone_name = models.CharField(max_length=200)
    zone_type = models.CharField(max_length=50, choices=[
        ('evacuation_center', 'Evacuation Center'),
        ('safe_zone', 'Safe Zone'),
        ('emergency_shelter', 'Emergency Shelter'),
        ('medical_facility', 'Medical Facility'),
    ])
    location = models.JSONField()  # {lat: float, lng: float}
    capacity = models.IntegerField(default=0)
    current_occupancy = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    facilities = models.JSONField(default=list)  # List of available facilities
    contact_number = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.zone_name} ({self.zone_type})"


class FraudDetection(models.Model):
    """AI-driven fraud detection system."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fraud_detections')
    fraud_type = models.CharField(max_length=50, choices=[
        ('payment_fraud', 'Payment Fraud'),
        ('identity_theft', 'Identity Theft'),
        ('account_takeover', 'Account Takeover'),
        ('phishing', 'Phishing'),
        ('malware', 'Malware'),
        ('social_engineering', 'Social Engineering'),
    ])
    risk_score = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1)])
    confidence_level = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1)])
    description = models.TextField()
    indicators = models.JSONField()  # List of suspicious indicators
    is_blocked = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.fraud_type} (Risk: {self.risk_score})"


class SecurityIncident(models.Model):
    """Security incident reporting."""
    incident_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='security_incidents')
    incident_type = models.CharField(max_length=50, choices=[
        ('theft', 'Theft'),
        ('assault', 'Assault'),
        ('vandalism', 'Vandalism'),
        ('suspicious_activity', 'Suspicious Activity'),
        ('cyber_attack', 'Cyber Attack'),
        ('data_breach', 'Data Breach'),
        ('other', 'Other'),
    ])
    location = models.JSONField()  # {lat: float, lng: float}
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('reported', 'Reported'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], default='reported')
    evidence = models.JSONField(default=list)  # List of evidence files/links
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Incident {self.incident_id} - {self.incident_type}"


class SafetyCheck(models.Model):
    """Regular safety check-ins."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='safety_checks')
    check_type = models.CharField(max_length=50, choices=[
        ('location_check', 'Location Check'),
        ('wellness_check', 'Wellness Check'),
        ('emergency_check', 'Emergency Check'),
        ('travel_safety', 'Travel Safety'),
    ])
    location = models.JSONField()  # {lat: float, lng: float}
    status = models.CharField(max_length=20, choices=[
        ('safe', 'Safe'),
        ('unsafe', 'Unsafe'),
        ('need_help', 'Need Help'),
        ('emergency', 'Emergency'),
    ])
    message = models.TextField(blank=True)
    is_automated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.check_type} ({self.status})"


class EmergencyContact(models.Model):
    """Emergency contacts for users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    is_primary = models.BooleanField(default=False)
    notification_preferences = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'name']

    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.relationship})"


class SafetyNotification(models.Model):
    """Safety notifications and alerts."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='safety_notifications')
    notification_type = models.CharField(max_length=50, choices=[
        ('disaster_alert', 'Disaster Alert'),
        ('fraud_alert', 'Fraud Alert'),
        ('security_alert', 'Security Alert'),
        ('safety_reminder', 'Safety Reminder'),
        ('emergency_contact', 'Emergency Contact'),
    ])
    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ])
    is_read = models.BooleanField(default=False)
    action_required = models.BooleanField(default=False)
    action_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}" 