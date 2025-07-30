from django.db import models
from django.forms import ValidationError
from accounts.models import User


class Locations(models.Model):
    name = models.CharField(
        max_length=100,
    )

    class Meta:
        db_table = "restaurants_locations"
        verbose_name_plural = "locations"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "restaurants_food_category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    owner_name = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    featured_image = models.ImageField(upload_to="restaurants/images/")
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    outlet = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    working_days = models.JSONField(blank=True, null=True)
    categories = models.ManyToManyField(Category)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    offer_text = models.CharField(max_length=50, blank=True, null=True)
    delivery_time = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "restaurants_restaurant"
        ordering = ["id"]

    def save(self, *args, **kwargs):
        if self.owner_name.role != "restaurant_owner":
            raise ValidationError(
                f"The user {self.owner_name} is not a restaurant owner."
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    VEGETARIAN_CHOICES = [
        ("veg", "Vegetarian"),
        ("non-veg", "Non-Vegetarian"),
    ]

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="food_items"
    )
    image = models.ImageField(upload_to="food_items/images/", blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    food_type = models.CharField(
        max_length=10, choices=VEGETARIAN_CHOICES, default="non-veg"
    )
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name="food_items")
    is_available = models.BooleanField(default=False)

    class Meta:
        db_table = "restaurants_food_items"

    def __str__(self):
        return self.name
