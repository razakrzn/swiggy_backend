from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from restaurants.models import Locations
from .serializers import LocationsSerializer


class LocationsList(APIView):
    def get(self, request):
        locations = Locations.objects.all()
        serializer = LocationsSerializer(locations, many=True)
        return Response(serializer.data)
