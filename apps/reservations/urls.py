from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("reservations/", views.reservation_list, name="reservation-list"),
    path("reservations/new/", views.reservation_form, name="reservation-form"),
    path("reservations/<int:pk>/", views.confirmation, name="confirmation"),
    path("redirect/", views.redirect_page, name="redirect-page"),
]
