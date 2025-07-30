from django.urls import path
from .views import (
    OrderListCreateView,
    OrderView,
    OrderDetailView,
    RestaurantOrderListView,
    OrderItemListCreateView,
    OrderItemDetailView,
)

urlpatterns = [
    # Orders URLs
    path("", OrderView.as_view(), name="orders"),
    path("orders-create/", OrderListCreateView.as_view(), name="order-list-create"),
    path(
        "orders-list/<int:pk>/", OrderDetailView.as_view(), name="order-list-detail"
    ),  # Retrieve, update, delete a specific order
    # Restaurant-specific Orders
    path(
        "restaurant-orders/",
        RestaurantOrderListView.as_view(),
        name="restaurant-order-list",
    ),  # List restaurant-specific orders
    # Order Items URLs
    path(
        "order-items/", OrderItemListCreateView.as_view(), name="order-item-list-create"
    ),  # List and create order items
    path(
        "order-items/<int:pk>/", OrderItemDetailView.as_view(), name="order-item-detail"
    ),  # Retrieve, update, delete a specific order item
]
