# UrbanEase MVP - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone and Setup
```bash
# Navigate to your project directory
cd urbanease

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Quick Setup
```bash
# Run the setup script (creates sample data and runs migrations)
python setup.py

# OR run manually:
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Step 3: Start the Application
```bash
# Option 1: Use the run script
python run.py

# Option 2: Use Django directly
python manage.py runserver
```

### Step 4: Access the Application
- **Main Application**: http://localhost:8000
- **Admin Interface**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/

## 🎯 Key Features to Explore

### 1. Smart Mobility
- **Real-time Transport Tracking**: `/api/mobility/routes/`
- **Smart Parking**: `/api/mobility/parking/`
- **EV Charging**: `/api/mobility/ev-charging/`
- **Traffic Management**: `/api/mobility/traffic/`

### 2. Smart Health
- **Health Profiles**: `/api/health/profiles/`
- **Health Metrics**: `/api/health/metrics/`
- **Telemedicine**: `/api/health/telemedicine/`
- **Emergency Services**: `/api/health/emergency/`

### 3. Smart Safety
- **Disaster Alerts**: `/api/safety/alerts/`
- **Safety Zones**: `/api/safety/zones/`
- **Fraud Detection**: `/api/safety/fraud/`
- **Security Incidents**: `/api/safety/incidents/`

### 4. Smart Services
- **Automated Services**: `/api/services/services/`
- **Self-Service Options**: `/api/services/self-service/`
- **Service Requests**: `/api/services/requests/`
- **Service Feedback**: `/api/services/feedback/`

### 5. Eco Points System
- **User Points**: `/api/users/eco-points/`
- **Leaderboard**: `/api/users/eco-points/leaderboard/`

## 🔧 API Testing

### Using curl
```bash
# Get all transport routes
curl http://localhost:8000/api/mobility/routes/

# Search for parking spots
curl -X POST http://localhost:8000/api/mobility/parking/search_parking/ \
  -H "Content-Type: application/json" \
  -d '{"location": {"lat": 40.7128, "lng": -74.0060}, "radius": 5.0}'

# Get health metrics
curl http://localhost:8000/api/health/metrics/latest_metrics/
```

### Using Postman
1. Import the API collection (if available)
2. Set base URL to `http://localhost:8000`
3. Test different endpoints

## 📊 Admin Interface

Access the comprehensive admin interface at `http://localhost:8000/admin/` to:

- **Manage Users**: Create, edit, and manage user profiles
- **Transport Data**: Add routes, vehicles, and parking spots
- **Health Records**: Monitor health metrics and alerts
- **Safety Zones**: Configure emergency shelters and safety zones
- **Service Management**: Manage automated services and categories

## 🎮 Demo Data

The setup script creates sample data including:
- Demo user account
- Service categories (Transportation, Health, Safety, etc.)
- Sample automated services
- Basic configuration

## 🔍 Troubleshooting

### Common Issues

1. **Import Error**: Make sure you're in the correct directory and virtual environment is activated
2. **Database Error**: Run `python manage.py migrate` to apply migrations
3. **Port Already in Use**: Change port with `python manage.py runserver 8001`
4. **Permission Error**: Make sure you have write permissions in the project directory

### Debug Mode
- Set `DEBUG=True` in `urbanease/settings.py` for detailed error messages
- Check Django logs in the console output

## 📱 Mobile App Integration

The API is designed for mobile app integration:
- CORS enabled for cross-origin requests
- Token-based authentication
- JSON API responses
- Real-time WebSocket support

## 🚀 Next Steps

1. **Customize the Application**:
   - Modify models in `*/models.py`
   - Add new API endpoints in `*/views.py`
   - Update serializers in `*/serializers.py`

2. **Add Real Data**:
   - Integrate with real transport APIs
   - Connect to health monitoring devices
   - Implement actual payment processing

3. **Deploy to Production**:
   - Set up PostgreSQL database
   - Configure Redis for caching
   - Set up HTTPS and security headers
   - Deploy to cloud platform (AWS, Google Cloud, etc.)

## 📞 Support

- **Documentation**: Check the main README.md
- **Issues**: Create an issue in the repository
- **Questions**: Contact the development team

---

**Happy coding! 🎉**

UrbanEase - Making urban living smarter, safer, and more sustainable! 🏙️✨ 