from django.urls import path

from . import views

urlpatterns = [
    # Display the home page when accessing the base "/reservations/"
    path("", views.home, name="home"),
    
    # Display the list when accessing "/reservations/list/"
    path("list/", views.reservation_list, name="reservation-list"),
    
    # Display the form when accessing "/reservations/new/"
    path("new/", views.reservation_form, name="reservation-form"),
    
    # Display the confirmation page when accessing "/reservations/<pk>/"
    path("<int:pk>/", views.confirmation, name="confirmation"),
    
    # Redirect route
    path("redirect/", views.redirect_page, name="redirect-page"),
    
    # HTMX partial route for available tables
    path(
        "available-tables-partial/",
        views.available_tables_partial,
        name="available-tables-partial",
    ),
]