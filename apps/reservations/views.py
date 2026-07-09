from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReservationForm
from .models import Reservation


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "reservations/home.html", {"now": datetime.now()})


def reservation_list(request: HttpRequest) -> HttpResponse:
    reservations = Reservation.objects.select_related("table").all()
    return render(request, "reservations/list.html", {"reservations": reservations})


def reservation_form(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            return redirect("confirmation", pk=reservation.pk)
    else:
        form = ReservationForm()
    return render(request, "reservations/form.html", {"form": form})


def confirmation(request: HttpRequest, pk: int) -> HttpResponse:
    reservation = get_object_or_404(Reservation.objects.select_related("table"), pk=pk)
    return render(
        request, "reservations/confirmation.html", {"reservation": reservation}
    )


def redirect_page(request: HttpRequest) -> HttpResponse:
    return redirect("reservation-list")
