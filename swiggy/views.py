from django.http import JsonResponse


def home_view(request):
    return JsonResponse(
        {"message": "Welcome to the API! Use /api/v1/ for the endpoints."}
    )
