from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.reservations.forms import ReservationForm
from apps.reservations.models import Reservation, Table


class ReservationFormValidationTests(TestCase):
    def setUp(self):
        self.table = Table.objects.create(table_number="T1", capacity=4)

    def test_past_reservation_time(self):
        dt = timezone.localtime(timezone.now() - timedelta(hours=1))
        form = ReservationForm(
            data={
                "customer_name": "Tanaka",
                "num_guests": 2,
                "reservation_time": dt.strftime("%Y-%m-%dT%H:%M"),
                "table": self.table.pk,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("reservation_time", form.errors)

    def test_exceeds_table_capacity(self):
        dt = timezone.localtime(timezone.now() + timedelta(days=1))
        form = ReservationForm(
            data={
                "customer_name": "Tanaka",
                "num_guests": 10,
                "reservation_time": dt.strftime("%Y-%m-%dT%H:%M"),
                "table": self.table.pk,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("num_guests", form.errors)

    def test_double_booking(self):
        dt = timezone.localtime(
            (timezone.now() + timedelta(days=1)).replace(
                microsecond=0, second=0
            )
        )
        Reservation.objects.create(
            customer_name="Sato",
            num_guests=2,
            reservation_time=dt,
            table=self.table,
        )
        form = ReservationForm(
            data={
                "customer_name": "Tanaka",
                "num_guests": 2,
                "reservation_time": dt.strftime("%Y-%m-%dT%H:%M"),
                "table": self.table.pk,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
