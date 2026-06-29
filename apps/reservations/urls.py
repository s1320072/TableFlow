from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("reservations/", views.reservation_list, name="reservation-list"),
    path("reservations/new/", views.reservation_form, name="reservation-form"),
    path(
        "reservations/process/",
        views.process_reservation,
        name="process-reservation",
    ),
    path("redirect/", views.redirect_page, name="redirect-page"),
]
