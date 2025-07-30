from rest_framework import generics, permissions, status
from rest_framework.response import Response
from orders.models import Order, OrderItem
from restaurants.models import Restaurant
from .serializers import OrderSerializer, OrderItemSerializer


# View for users to create orders and list their own orders
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}

    def get_queryset(self):
        # Users can only see their own orders
        return Order.objects.filter(user=self.request.user, is_deleted=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()  # Save the order and associate it with the user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.is_deleted = True
        instance.save()

        return Response(
            {"detail": "Order marked as deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {"request": self.request}

    def get_queryset(self):
        restaurant = Restaurant.objects.filter(owner_name=self.request.user).first()
        if restaurant:
            return Order.objects.filter(restaurant=restaurant)
        return Order.objects.all()


# View for restaurant owners to list orders related to their restaurant
class RestaurantOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Fetch orders for the restaurant owned by the current user
        restaurant = Restaurant.objects.filter(owner_name=self.request.user).first()
        if restaurant:
            return Order.objects.filter(restaurant=restaurant)
        return Order.objects.none()


# View for restaurant owners to update the status of an order
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        order = self.get_object()

        # Ensure only the restaurant owner can update the order
        if request.user != order.restaurant.owner_name:
            return Response(
                {"error": "You are not authorized to update this order."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Validate the status field
        if (
            "status" in request.data
            and request.data["status"] not in dict(Order.STATUS_CHOICES).keys()
        ):
            return Response(
                {"error": "Invalid status choice."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View to create and list order items
class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the order item
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View to update, retrieve, and delete specific order items
class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
