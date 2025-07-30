from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from restaurants.models import Restaurant

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("restaurant_owner", "Restaurant Owner"),
        ("admin", "Admin"),
    )

    role = serializers.ChoiceField(choices=ROLE_CHOICES)  # Restrict valid role options
    restaurant_ids = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role", "restaurant_ids"]
        extra_kwargs = {
            "password": {"write_only": True},  # Hide password in API responses
        }

    def get_restaurant_ids(self, obj):
        # Fetch the first restaurant ID for the user if they are a restaurant owner
        if obj.role == "restaurant_owner":
            restaurant = Restaurant.objects.filter(owner_name=obj).first()
            return restaurant.id if restaurant else None
        return None

    def create(self, validated_data):
        """
        Override create method to hash the password before saving the User instance.
        """
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
