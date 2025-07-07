import requests
import json
from datetime import datetime
from django.conf import settings
from decouple import config

class WeatherService:
    """Weather service for Kolkata using OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = config('OPENWEATHER_API_KEY', default='demo_key')
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.kolkata_coords = {
            'lat': 22.5726,
            'lon': 88.3639
        }
    
    def get_current_weather(self):
        """Get current weather for Kolkata"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': self.kolkata_coords['lat'],
                'lon': self.kolkata_coords['lon'],
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'visibility': data.get('visibility', 10000),
                'clouds': data['clouds']['all'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
                'city': 'Kolkata',
                'country': 'IN',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            # Return demo data if API fails
            return self.get_demo_weather()
    
    def get_weather_forecast(self):
        """Get 5-day weather forecast for Kolkata"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': self.kolkata_coords['lat'],
                'lon': self.kolkata_coords['lon'],
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            forecast = []
            
            for item in data['list'][:8]:  # Next 24 hours (3-hour intervals)
                forecast.append({
                    'datetime': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M'),
                    'temperature': item['main']['temp'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed']
                })
            
            return forecast
        except Exception as e:
            return self.get_demo_forecast()
    
    def get_weather_alerts(self):
        """Get weather alerts for Kolkata"""
        try:
            url = f"{self.base_url}/onecall"
            params = {
                'lat': self.kolkata_coords['lat'],
                'lon': self.kolkata_coords['lon'],
                'appid': self.api_key,
                'exclude': 'current,minutely,hourly,daily',
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            alerts = []
            
            if 'alerts' in data:
                for alert in data['alerts']:
                    alerts.append({
                        'event': alert['event'],
                        'description': alert['description'],
                        'start': datetime.fromtimestamp(alert['start']).strftime('%Y-%m-%d %H:%M'),
                        'end': datetime.fromtimestamp(alert['end']).strftime('%Y-%m-%d %H:%M'),
                        'severity': alert.get('tags', ['moderate'])[0]
                    })
            
            return alerts
        except Exception as e:
            return self.get_demo_alerts()
    
    def get_demo_weather(self):
        """Demo weather data for Kolkata"""
        return {
            'temperature': 32.5,
            'feels_like': 35.2,
            'humidity': 78,
            'pressure': 1013,
            'description': 'scattered clouds',
            'icon': '03d',
            'wind_speed': 3.2,
            'wind_direction': 180,
            'visibility': 10000,
            'clouds': 40,
            'sunrise': '05:30',
            'sunset': '18:45',
            'city': 'Kolkata',
            'country': 'IN',
            'timestamp': datetime.now().isoformat()
        }
    
    def get_demo_forecast(self):
        """Demo forecast data"""
        return [
            {
                'datetime': '2024-07-07 12:00',
                'temperature': 32.5,
                'description': 'scattered clouds',
                'icon': '03d',
                'humidity': 78,
                'wind_speed': 3.2
            },
            {
                'datetime': '2024-07-07 15:00',
                'temperature': 31.8,
                'description': 'light rain',
                'icon': '10d',
                'humidity': 82,
                'wind_speed': 4.1
            },
            {
                'datetime': '2024-07-07 18:00',
                'temperature': 29.5,
                'description': 'clear sky',
                'icon': '01n',
                'humidity': 85,
                'wind_speed': 2.8
            }
        ]
    
    def get_demo_alerts(self):
        """Demo weather alerts"""
        return [
            {
                'event': 'Heavy Rain',
                'description': 'Heavy rainfall expected in Kolkata and surrounding areas',
                'start': '2024-07-07 14:00',
                'end': '2024-07-07 20:00',
                'severity': 'moderate'
            },
            {
                'event': 'High Humidity',
                'description': 'High humidity levels may cause discomfort',
                'start': '2024-07-07 10:00',
                'end': '2024-07-07 18:00',
                'severity': 'minor'
            }
        ]

# Global weather service instance
weather_service = WeatherService() 