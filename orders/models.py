from django.db import models
from django.utils.timezone import now
from accounts.models import User
from restaurants.models import Restaurant, FoodItem


class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]
    order_id = models.CharField(max_length=15, unique=True, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="orders"
    )
    total_price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    customer_location = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.order_id:
            # Generate a unique order ID
            import uuid

            self.order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    menu_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.menu_item.name} in Order {self.order.id}"
