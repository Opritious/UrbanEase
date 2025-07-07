#!/usr/bin/env python3
"""
UrbanEase Setup Script
Initializes the Django project with basic data and configuration.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from django.utils import timezone

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urbanease.settings')
django.setup()

def create_sample_data():
    """Create sample data for the UrbanEase MVP."""
    print("Creating sample data for UrbanEase...")
    
    # Create a sample user if none exists
    if not User.objects.filter(username='demo_user').exists():
        user = User.objects.create_user(
            username='demo_user',
            email='demo@urbanease.com',
            password='demo123456',
            first_name='Demo',
            last_name='User'
        )
        print(f"Created demo user: {user.username}")
    
    print("Sample data creation completed!")

def main():
    """Main setup function."""
    print("🚀 UrbanEase MVP Setup")
    print("=" * 50)
    
    # Check if Django is properly configured
    try:
        from django.conf import settings
        print("✅ Django settings loaded successfully")
    except Exception as e:
        print(f"❌ Error loading Django settings: {e}")
        return
    
    # Run migrations
    print("\n📦 Running database migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed successfully")
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return
    
    # Create sample data
    print("\n📊 Creating sample data...")
    try:
        create_sample_data()
        print("✅ Sample data created successfully")
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
    
    print("\n🎉 UrbanEase setup completed!")
    print("\nNext steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Run the development server: python manage.py runserver")
    print("3. Access the admin interface: http://localhost:8000/admin")
    print("4. Explore the API: http://localhost:8000/api/")

if __name__ == '__main__':
    main() 