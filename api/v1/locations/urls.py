from django.urls import path
from .views import LocationsList


urlpatterns = [
    path("", LocationsList.as_view(), name="Locations-list"),
]
