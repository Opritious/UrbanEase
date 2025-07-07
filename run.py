#!/usr/bin/env python3
"""
UrbanEase Run Script
Quick start script for the UrbanEase Django application.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import django
        print("✅ Django is installed")
    except ImportError:
        print("❌ Django is not installed. Please run: pip install -r requirements.txt")
        return False
    
    try:
        import rest_framework
        print("✅ Django REST Framework is installed")
    except ImportError:
        print("❌ Django REST Framework is not installed. Please run: pip install -r requirements.txt")
        return False
    
    return True

def setup_environment():
    """Set up the environment for running the application."""
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urbanease.settings')
    
    # Add the project directory to Python path
    project_dir = Path(__file__).parent
    sys.path.insert(0, str(project_dir))

def run_migrations():
    """Run database migrations."""
    print("📦 Running database migrations...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✅ Migrations completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        return False

def create_superuser():
    """Create a superuser if none exists."""
    try:
        import django
        django.setup()
        from django.contrib.auth.models import User
        
        if not User.objects.filter(is_superuser=True).exists():
            print("👤 No superuser found. Creating one...")
            print("Please enter the following details:")
            
            username = input("Username (admin): ") or "admin"
            email = input("Email: ") or "admin@urbanease.com"
            password = input("Password: ") or "admin123456"
            
            User.objects.create_superuser(username, email, password)
            print(f"✅ Superuser '{username}' created successfully")
        else:
            print("✅ Superuser already exists")
        
        return True
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        return False

def start_server():
    """Start the Django development server."""
    print("🚀 Starting UrbanEase development server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("🔧 Admin interface: http://localhost:8000/admin")
    print("📚 API documentation: http://localhost:8000/api/")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main function to run the UrbanEase application."""
    print("🏙️  UrbanEase - Smart Urban Living Platform")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Setup environment
    setup_environment()
    
    # Run migrations
    if not run_migrations():
        return
    
    # Create superuser
    if not create_superuser():
        return
    
    # Start server
    start_server()

if __name__ == '__main__':
    main() 