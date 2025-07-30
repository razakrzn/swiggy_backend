import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from restaurants.models import Restaurant, FoodItem
from .serializers import RestaurantSerializer, FoodItemSerializer
from .pagination import StandardResultSetPagination


class RestaurantList(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        restaurants = Restaurant.objects.all()

        query = request.GET.get("q")
        if query:
            restaurants = restaurants.filter(name__icontains=query)

        pagination = StandardResultSetPagination()
        paginated_restaurants = pagination.paginate_queryset(restaurants, request)

        serializer = RestaurantSerializer(
            paginated_restaurants, many=True, context={"request": request}
        )

        response_data = {
            "status_code": 6000,
            "count": pagination.page.paginator.count,
            "next": pagination.get_next_link(),
            "previous": pagination.get_previous_link(),
            "data": serializer.data,
        }

        return Response(response_data)

    def post(self, request):
        serializer = RestaurantSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status_code": 201,
                    "message": "Restaurant created successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "status_code": 400,
                "message": "Restaurant creation failed.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class RestaurantDetails(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:

            restaurant = Restaurant.objects.get(pk=pk)

            serializer = RestaurantSerializer(restaurant, context={"request": request})
            restaurant_data = serializer.data

            food_menu = [
                item
                for item in restaurant_data.get("food_menu", [])
                if not item.get("is_available", False)
            ]

            restaurant_data["food_menu"] = food_menu

            return Response(
                {
                    "status_code": 6000,
                    "data": restaurant_data,
                },
                status=status.HTTP_200_OK,
            )

        except Restaurant.DoesNotExist:
            return Response(
                {
                    "status_code": 6001,
                    "message": "Restaurant not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class FoodItemList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk: int) -> Response:
        try:
            food_item = FoodItem.objects.get(pk=pk, is_available=False)
            serializer = FoodItemSerializer(food_item, context={"request": request})
            return Response(
                {
                    "status_code": 6000,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except FoodItem.DoesNotExist:
            return Response(
                {
                    "status_code": 6001,
                    "message": "Food item not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class FoodItems(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        food_items = FoodItem.objects.filter(is_available=False)

        serializer = FoodItemSerializer(
            food_items, many=True, context={"request": request}
        )

        response_data = {
            "status_code": 6000,
            "data": serializer.data,
        }

        return Response(response_data)


class FoodItemCreateView(APIView):
    def post(self, request):
        data = request.data.copy()
        data["restaurant"] = data.get("restaurant")  # Ensure it's an ID, not an object
        serializer = FoodItemSerializer(data=data)
        # serializer = FoodItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
