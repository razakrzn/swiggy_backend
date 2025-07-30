from django.urls import path
from .views import (
    RestaurantList,
    FoodItemList,
    RestaurantDetails,
    FoodItems,
    FoodItemCreateView,
)

urlpatterns = [
    path("", RestaurantList.as_view(), name="restaurant-list"),
    path("<int:pk>/", RestaurantDetails.as_view(), name="restaurantDetails-list"),
    path("food-items/", FoodItems.as_view(), name="food_item"),
    path("food-item/<int:pk>/", FoodItemList.as_view(), name="fooditem-detail"),
    path("create-food-items/", FoodItemCreateView.as_view(), name="create-food-item"),
]
