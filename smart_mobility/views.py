from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import (
    TransportRoute, TransportVehicle, ParkingSpot, EVChargingStation,
    TrafficData, UserTransportActivity
)
from .serializers import (
    TransportRouteSerializer, TransportVehicleSerializer, ParkingSpotSerializer,
    EVChargingStationSerializer, TrafficDataSerializer, UserTransportActivitySerializer,
    RouteSearchSerializer, ParkingSearchSerializer, EVChargingSearchSerializer
)


class TransportViewSet(viewsets.ModelViewSet):
    queryset = TransportRoute.objects.all()
    serializer_class = TransportRouteSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def search_routes(self, request):
        """Search for transport routes between two points."""
        serializer = RouteSearchSerializer(data=request.data)
        if serializer.is_valid():
            # Simulate route search logic
            start = serializer.validated_data['start_location']
            end = serializer.validated_data['end_location']
            
            # Mock route results
            routes = TransportRoute.objects.filter(is_active=True)[:5]
            serializer = self.get_serializer(routes, many=True)
            return Response({
                'routes': serializer.data,
                'search_params': serializer.validated_data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def vehicles(self, request, pk=None):
        """Get real-time vehicles for a specific route."""
        route = self.get_object()
        vehicles = route.vehicles.filter(status='active')
        serializer = TransportVehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def nearby_routes(self, request):
        """Get routes near user's location."""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        
        if lat and lng:
            # Mock nearby routes logic
            routes = TransportRoute.objects.filter(is_active=True)[:10]
            serializer = self.get_serializer(routes, many=True)
            return Response(serializer.data)
        return Response({'error': 'Location parameters required'}, status=status.HTTP_400_BAD_REQUEST)


class ParkingViewSet(viewsets.ModelViewSet):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def search_parking(self, request):
        """Search for available parking spots."""
        serializer = ParkingSearchSerializer(data=request.data)
        if serializer.is_valid():
            location = serializer.validated_data['location']
            radius = serializer.validated_data['radius']
            spot_type = serializer.validated_data.get('spot_type')
            
            # Mock parking search logic
            spots = ParkingSpot.objects.filter(is_available=True)
            if spot_type:
                spots = spots.filter(spot_type=spot_type)
            
            serializer = self.get_serializer(spots[:20], many=True)
            return Response({
                'parking_spots': serializer.data,
                'search_params': serializer.validated_data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def available_spots(self, request):
        """Get all available parking spots."""
        spots = ParkingSpot.objects.filter(is_available=True)
        serializer = self.get_serializer(spots, many=True)
        return Response(serializer.data)


class EVChargingViewSet(viewsets.ModelViewSet):
    queryset = EVChargingStation.objects.all()
    serializer_class = EVChargingStationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def search_charging(self, request):
        """Search for EV charging stations."""
        serializer = EVChargingSearchSerializer(data=request.data)
        if serializer.is_valid():
            location = serializer.validated_data['location']
            radius = serializer.validated_data['radius']
            charger_type = serializer.validated_data.get('charger_type')
            
            # Mock charging station search logic
            stations = EVChargingStation.objects.filter(is_available=True)
            if charger_type:
                stations = stations.filter(charger_type=charger_type)
            
            serializer = self.get_serializer(stations[:15], many=True)
            return Response({
                'charging_stations': serializer.data,
                'search_params': serializer.validated_data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def start_charging(self, request, pk=None):
        """Start charging at a station."""
        station = self.get_object()
        if station.is_available and not station.current_user:
            station.current_user = request.user
            station.is_available = False
            station.save()
            return Response({'message': 'Charging started successfully'})
        return Response({'error': 'Station not available'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def stop_charging(self, request, pk=None):
        """Stop charging at a station."""
        station = self.get_object()
        if station.current_user == request.user:
            station.current_user = None
            station.is_available = True
            station.save()
            return Response({'message': 'Charging stopped successfully'})
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)


class TrafficViewSet(viewsets.ModelViewSet):
    queryset = TrafficData.objects.all()
    serializer_class = TrafficDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def current_traffic(self, request):
        """Get current traffic conditions."""
        # Get latest traffic data
        traffic_data = TrafficData.objects.all()[:50]
        serializer = self.get_serializer(traffic_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def report_incident(self, request):
        """Report traffic incident."""
        location = request.data.get('location')
        description = request.data.get('description')
        
        if location and description:
            TrafficData.objects.create(
                location=location,
                traffic_level='severe',
                average_speed=0,
                congestion_index=1.0,
                incident_reported=True,
                incident_description=description
            )
            return Response({'message': 'Incident reported successfully'})
        return Response({'error': 'Location and description required'}, status=status.HTTP_400_BAD_REQUEST)


class UserTransportActivityViewSet(viewsets.ModelViewSet):
    queryset = UserTransportActivity.objects.all()
    serializer_class = UserTransportActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserTransportActivity.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def trip_history(self, request):
        """Get user's trip history."""
        activities = self.get_queryset()
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def carbon_savings(self, request):
        """Get user's carbon savings."""
        total_saved = sum(activity.carbon_saved for activity in self.get_queryset())
        return Response({'total_carbon_saved': total_saved})

    @action(detail=False, methods=['get'])
    def monthly_stats(self, request):
        """Get monthly transport statistics."""
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        month_ago = now - timedelta(days=30)
        
        monthly_activities = self.get_queryset().filter(timestamp__gte=month_ago)
        
        stats = {
            'total_trips': monthly_activities.count(),
            'total_distance': sum(activity.distance for activity in monthly_activities),
            'total_carbon_saved': sum(activity.carbon_saved for activity in monthly_activities),
            'total_cost': sum(activity.cost for activity in monthly_activities),
        }
        
        return Response(stats) 