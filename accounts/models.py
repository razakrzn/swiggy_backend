from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = "admin"
    CUSTOMER = "customer"
    RESTAURANT_OWNER = "restaurant_owner"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (CUSTOMER, "Customer"),
        (RESTAURANT_OWNER, "Restaurant Owner"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ADMIN)

    def __str__(self):
        return self.username
