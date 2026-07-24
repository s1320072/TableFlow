from django.test import TestCase

from apps.reservations.models import Reservation, Table


class TableModelTests(TestCase):
    def test_str(self):
        table = Table(table_number="A1", capacity=4)
        self.assertEqual(str(table), "Table A1 (4 seats)")

    def test_default_is_active(self):
        table = Table.objects.create(table_number="T1", capacity=2)
        self.assertTrue(table.is_active)


class ReservationModelTests(TestCase):
    def setUp(self):
        self.table = Table.objects.create(table_number="T1", capacity=4)

    def test_str(self):
        r = Reservation.objects.create(
            customer_name="Tanaka",
            num_guests=2,
            reservation_time="2026-08-01T19:00:00",
            table=self.table,
        )
        self.assertIn("Tanaka", str(r))
        self.assertIn("2 guests", str(r))

    def test_default_status(self):
        r = Reservation.objects.create(
            customer_name="Sato",
            num_guests=2,
            reservation_time="2026-08-01T19:00:00",
            table=self.table,
        )
        self.assertEqual(r.status, "PENDING")
