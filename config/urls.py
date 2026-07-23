from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.api.urls")),
    path("reservations/", include("apps.reservations.urls")),
    path("", RedirectView.as_view(url="/reservations/", permanent=False)),
]
