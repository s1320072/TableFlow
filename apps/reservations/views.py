from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "reservations/home.html", {"now": datetime.now()})


def reservation_list(request: HttpRequest) -> HttpResponse:
    mock_reservations = [
        {"id": 1, "customer_name": "Alice", "num_guests": 2,
         "table_number": "T1", "time": "2026-06-29 18:00", "status": "CONFIRMED"},
        {"id": 2, "customer_name": "Bob", "num_guests": 4,
         "table_number": "T3", "time": "2026-06-29 19:00", "status": "PENDING"},
        {"id": 3, "customer_name": "Charlie", "num_guests": 6,
         "table_number": "T5", "time": "2026-06-30 20:00", "status": "CONFIRMED"},
    ]
    return render(
        request, "reservations/list.html", {"reservations": mock_reservations}
    )


def reservation_form(request: HttpRequest) -> HttpResponse:
    return render(request, "reservations/form.html")


def process_reservation(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        data = {
            "customer_name": request.POST.get("customer_name"),
            "num_guests": request.POST.get("num_guests"),
            "reservation_time": request.POST.get("reservation_time"),
        }
        return render(request, "reservations/confirmation.html", {"data": data})
    return redirect("reservation-form")


def redirect_page(request: HttpRequest) -> HttpResponse:
    return redirect("reservation-list")
