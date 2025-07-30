from rest_framework import serializers
from restaurants.models import Locations


class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ["id", "name"]
