from rest_framework import serializers
from orders.models import Order, OrderItem
from restaurants.models import Restaurant, FoodItem


class FoodItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = FoodItem
        fields = ["id", "name", "price", "image"]

    def get_image(self, obj):
        request = self.context.get("request")
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            # Fallback to a default base URL if request is not available
            base_url = "http://localhost:8000"
            return f"{base_url}{obj.image.url}"
        return None


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "name"]


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.PrimaryKeyRelatedField(queryset=FoodItem.objects.all())

    class Meta:
        model = OrderItem
        fields = ["id", "menu_item", "quantity"]

    def to_representation(self, instance):
        # Customize the representation to include menu item details
        representation = super().to_representation(instance)
        representation["menu_item"] = FoodItemSerializer(instance.menu_item).data
        return representation


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all()  # Accept restaurant ID
    )
    # Add this line to include the username
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = [
            "id",
            "restaurant",
            "total_price",
            "status",
            "created_at",
            "order_items",
            "user",
            "customer_location",
            "customer_phone",
            "is_deleted",
        ]

    def get_order_items(self, obj):
        # Use MenuItemSerializer to serialize `menu_item` data
        return [
            {
                "id": item.id,
                "menu_item": FoodItemSerializer(
                    item.menu_item, context=self.context
                ).data,
                "quantity": item.quantity,
            }
            for item in obj.order_items.all()
        ]

    def create(self, validated_data):
        # Print validated data to inspect it
        print("Validated data:", validated_data)
        # Extract order items data
        order_items_data = validated_data.pop("order_items")

        # Get the user from the request context
        user = self.context["request"].user

        # Pop the restaurant from validated_data and create the order
        restaurant = validated_data.pop("restaurant")
        order = Order.objects.create(user=user, restaurant=restaurant, **validated_data)

        # Loop through each order item and create the corresponding OrderItem
        for item_data in order_items_data:
            # Get the menu_item ID from the data
            # Access menu_item id directly from the object
            menu_item_id = item_data["menu_item"].id

            # Create OrderItem with the associated order and menu_item
            OrderItem.objects.create(
                order=order,
                menu_item_id=menu_item_id,  # Use menu_item_id directly
                quantity=item_data["quantity"],
            )

        return order

    def to_representation(self, instance):
        # Customize the representation to include restaurant details
        representation = super().to_representation(instance)
        representation["restaurant"] = RestaurantSerializer(instance.restaurant).data

        # Include order items in the representation
        representation["order_items"] = OrderItemSerializer(
            instance.order_items.all(), many=True
        ).data
        return representation
