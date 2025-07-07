# UrbanEase - Smart City Platform

A comprehensive smart city platform for Kolkata with features including smart mobility, health, safety, and services.

## Features

- **Smart Mobility**: Real-time traffic monitoring, public transport tracking, and smart parking
- **Smart Health**: Telemedicine, health monitoring, and emergency response
- **Smart Safety**: Disaster alerts, fraud detection, and security monitoring with real-time weather data
- **Smart Services**: Digital services, citizen engagement, and smart governance

## Weather Integration

The platform includes real-time weather data for Kolkata using the OpenWeatherMap API:

- Current weather conditions
- Weather forecasts
- Weather alerts and warnings
- Automatic fallback to demo data if API is unavailable

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# OpenWeatherMap API (Optional)
OPENWEATHER_API_KEY=your-openweather-api-key-here

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0
```

### 3. Get OpenWeatherMap API Key (Optional)

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Add it to your `.env` file as `OPENWEATHER_API_KEY`

If no API key is provided, the system will use demo weather data.

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Run the Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Weather API
- `GET /api/v1/safety/weather/current/` - Current weather for Kolkata
- `GET /api/v1/safety/weather/forecast/` - Weather forecast
- `GET /api/v1/safety/weather/alerts/` - Weather alerts

### Safety API
- `GET /api/v1/safety/alerts/` - Disaster alerts
- `GET /api/v1/safety/zones/` - Safety zones
- `GET /api/v1/safety/fraud/` - Fraud detection
- `GET /api/v1/safety/incidents/` - Security incidents

### Mobility API
- `GET /api/v1/mobility/traffic/` - Traffic data
- `GET /api/v1/mobility/transport/` - Public transport
- `GET /api/v1/mobility/parking/` - Parking availability

### Health API
- `GET /api/v1/health/telemedicine/` - Telemedicine services
- `GET /api/v1/health/monitoring/` - Health monitoring
- `GET /api/v1/health/emergency/` - Emergency response

### Services API
- `GET /api/v1/services/digital/` - Digital services
- `GET /api/v1/services/engagement/` - Citizen engagement
- `GET /api/v1/services/governance/` - Smart governance

## Frontend Pages

- Home: `http://127.0.0.1:8000/`
- Smart Mobility: `http://127.0.0.1:8000/mobility/`
- Smart Health: `http://127.0.0.1:8000/health/`
- Smart Safety: `http://127.0.0.1:8000/safety/`
- Smart Services: `http://127.0.0.1:8000/services/`
- Login: `http://127.0.0.1:8000/login/`
- Register: `http://127.0.0.1:8000/register/`

## Weather Features

The weather integration provides:

1. **Real-time Weather Data**: Current temperature, humidity, wind speed, and visibility
2. **Weather Icons**: Dynamic icons based on weather conditions
3. **Weather Alerts**: Real-time alerts for severe weather conditions
4. **Fallback System**: Demo data when API is unavailable
5. **Auto-refresh**: Weather data updates every 5 minutes

## Technology Stack

- **Backend**: Django 4.2.7, Django REST Framework
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (default), PostgreSQL (production)
- **Weather API**: OpenWeatherMap
- **Real-time**: Django Channels, WebSockets
- **Task Queue**: Celery, Redis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## 🚀 Features

### Smart Mobility
- **Real-time Transport Tracking**: Live updates on buses, metro, trains, and bike sharing
- **AI-based Traffic Management**: Intelligent traffic monitoring and congestion reduction
- **Smart Parking Solutions**: Real-time parking spot availability and booking
- **Integrated Public Transport**: One-stop ticketing for all public transport modes
- **EV Charging Network**: Comprehensive electric vehicle charging station network

### Smart Health
- **Personalized Health Insights**: AI-driven health monitoring and risk assessment
- **Telemedicine Integration**: Remote consultations with healthcare providers
- **GPS-enabled Emergency Services**: Optimized ambulance and emergency response
- **Health Risk Alerts**: Early warnings for diseases and pollution-related risks
- **Health Metrics Tracking**: Comprehensive health data monitoring

### Smart Safety & Security
- **Disaster Alert System**: Real-time emergency notifications and evacuation guidance
- **AI-driven Fraud Detection**: Advanced security monitoring and threat prevention
- **Safety Zones**: Emergency shelters and safe zones mapping
- **Security Incident Reporting**: User-driven security incident management
- **Automated Safety Checks**: Regular safety monitoring and alerts

### Smart Services
- **Automated Services**: Streamlined urban service delivery
- **Self-Service Options**: User-friendly self-service capabilities
- **Service Scheduling**: Automated service scheduling and management
- **Feedback System**: Comprehensive user feedback and rating system

### Special Features
- **Eco Points System**: Reward system for sustainable urban choices
- **Carbon Footprint Tracking**: Environmental impact monitoring
- **Community Engagement**: User activity tracking and community features

## 🛠 Technology Stack

- **Backend**: Django 4.2.7
- **API**: Django REST Framework
- **Real-time**: Django Channels (WebSocket support)
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Authentication**: Django built-in + Token Authentication
- **Task Queue**: Celery with Redis
- **CORS**: django-cors-headers
- **Environment**: python-decouple

## 📁 Project Structure

```
urbanease/
├── urbanease/                 # Main project settings
│   ├── settings.py           # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── api_urls.py          # API URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration (WebSocket)
├── user_management/          # User profiles and eco points
├── smart_mobility/          # Transport and mobility features
├── smart_health/            # Health monitoring and telemedicine
├── smart_safety/            # Safety and security features
├── admin.py                 # Comprehensive admin interface
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd urbanease
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main app: http://localhost:8000
   - Admin interface: http://localhost:8000/admin
   - API documentation: http://localhost:8000/api/

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `POST /api/users/logout/` - User logout

### Smart Mobility APIs
- `GET /api/mobility/routes/` - Get transport routes
- `POST /api/mobility/routes/search_routes/` - Search routes
- `GET /api/mobility/parking/` - Get parking spots
- `POST /api/mobility/parking/search_parking/` - Search parking
- `GET /api/mobility/ev-charging/` - Get EV charging stations
- `GET /api/mobility/traffic/current_traffic/` - Get traffic data

### Smart Health APIs
- `GET /api/health/profiles/my_profile/` - Get health profile
- `GET /api/health/metrics/latest_metrics/` - Get health metrics
- `GET /api/health/alerts/active_alerts/` - Get health alerts
- `GET /api/health/telemedicine/upcoming_appointments/` - Get appointments
- `POST /api/health/emergency/request_emergency/` - Request emergency service

### Smart Safety APIs
- `GET /api/safety/alerts/active_alerts/` - Get disaster alerts
- `GET /api/safety/zones/nearby_zones/` - Get safety zones
- `GET /api/safety/fraud/active_detections/` - Get fraud detections
- `POST /api/safety/incidents/report_incident/` - Report security incident

### Eco Points APIs
- `GET /api/users/eco-points/total_points/` - Get total eco points
- `GET /api/users/eco-points/leaderboard/` - Get eco points leaderboard

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Database Configuration
The project is configured to use SQLite by default. For production, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'urbanease_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🎯 Key Features Implementation

### Real-time Updates
- WebSocket support for live transport tracking
- Real-time traffic updates
- Live emergency alerts

### AI Integration
- Health risk assessment algorithms
- Traffic pattern analysis
- Fraud detection systems
- Pollution monitoring

### Mobile-First Design
- Responsive API design
- CORS configuration for mobile apps
- Token-based authentication

### Scalability
- Modular app architecture
- Celery for background tasks
- Redis for caching and message queuing

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📊 Admin Interface

Access the comprehensive admin interface at `/admin/` to manage:
- User profiles and eco points
- Transport routes and vehicles
- Health metrics and alerts
- Safety zones and incidents
- Service categories and requests

## 🔒 Security Features

- Django's built-in security features
- CORS protection
- Token-based authentication
- Input validation and sanitization
- SQL injection protection

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG=False` in settings
2. Configure production database
3. Set up static file serving
4. Configure HTTPS
5. Set up monitoring and logging
6. Configure backup systems

### Docker Support (Future)
- Dockerfile for containerization
- docker-compose for multi-service deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🎉 Acknowledgments

- Django community for the excellent framework
- Urban planning experts for domain knowledge
- Smart city initiatives for inspiration

---

**UrbanEase** - Making urban living smarter, safer, and more sustainable! 🏙️✨ 