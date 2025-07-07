"""
URL configuration for UrbanEase project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/mobility/', include('smart_mobility.urls')),
    path('api/health/', include('smart_health.urls')),
    path('api/safety/', include('smart_safety.urls')),
    path('api/users/', include('user_management.urls')),
    path('api/', include('urbanease.api_urls')),
    
    # Frontend URLs
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('mobility/', TemplateView.as_view(template_name='mobility.html'), name='mobility'),
    path('health/', TemplateView.as_view(template_name='health.html'), name='health'),
    path('safety/', TemplateView.as_view(template_name='safety.html'), name='safety'),
    path('services/', TemplateView.as_view(template_name='home.html'), name='services'),
    path('eco-points/', TemplateView.as_view(template_name='eco-points.html'), name='eco-points'),
    path('about-us/', TemplateView.as_view(template_name='about-us.html'), name='about-us'),
    
    # Authentication URLs (placeholder)
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('logout/', TemplateView.as_view(template_name='home.html'), name='logout'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('settings/', TemplateView.as_view(template_name='settings.html'), name='settings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 