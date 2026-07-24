from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.reservations.models import Reservation, Table


class PageStatusTests(TestCase):
    def setUp(self):
        self.table = Table.objects.create(table_number="T1", capacity=4)

    def test_home(self):
        self.assertEqual(self.client.get("/reservations/").status_code, 200)

    def test_list(self):
        self.assertEqual(self.client.get("/reservations/list/").status_code, 200)

    def test_new(self):
        self.assertEqual(self.client.get("/reservations/new/").status_code, 200)

    def test_confirmation(self):
        r = Reservation.objects.create(
            customer_name="Tanaka",
            num_guests=2,
            reservation_time=timezone.now() + timedelta(days=1),
            table=self.table,
        )
        self.assertEqual(
            self.client.get(f"/reservations/{r.pk}/").status_code, 200
        )


class AvailableTablesPartialTests(TestCase):
    def setUp(self):
        self.small = Table.objects.create(table_number="S1", capacity=2)
        self.large = Table.objects.create(table_number="L1", capacity=6)
        self.inactive = Table.objects.create(
            table_number="X1", capacity=4, is_active=False
        )

    def test_no_params(self):
        resp = self.client.get("/reservations/available-tables-partial/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.small, resp.context["tables"])
        self.assertIn(self.large, resp.context["tables"])
        self.assertNotIn(self.inactive, resp.context["tables"])

    def test_filters_by_num_guests(self):
        resp = self.client.get(
            "/reservations/available-tables-partial/",
            {"num_guests": 5},
        )
        self.assertIn(self.large, resp.context["tables"])
        self.assertNotIn(self.small, resp.context["tables"])

    def test_filters_by_reservation_time(self):
        dt = timezone.now() + timedelta(days=1)
        Reservation.objects.create(
            customer_name="Sato",
            num_guests=2,
            reservation_time=dt,
            table=self.small,
        )
        resp = self.client.get(
            "/reservations/available-tables-partial/",
            {"reservation_time": dt.isoformat()},
        )
        self.assertNotIn(self.small, resp.context["tables"])
        self.assertIn(self.large, resp.context["tables"])
