from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from swiggy import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home_view, name="home"),
    path("api/v1/restaurants/", include("api.v1.restaurants.urls")),
    path("api/v1/categories/", include("api.v1.categories.urls")),
    path("api/v1/auth/", include("api.v1.auth.urls")),
    path("api/v1/orders/", include("api.v1.orders.urls")),
    path("api/v1/locations/", include("api.v1.locations.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
