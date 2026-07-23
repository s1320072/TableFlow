from django.db import models


class Table(models.Model):
    table_number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        # 1. capacity(定員)の昇順、2. table_number(テーブル番号)の昇順 で並び替え
        ordering = ["capacity", "table_number"]

    def __str__(self):
        return f"Table {self.table_number} ({self.capacity} seats)"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "承認待ち"),
        ("CONFIRMED", "予約確定"),
        ("CANCELLED", "キャンセル"),
    ]
    customer_name = models.CharField(max_length=100)
    num_guests = models.PositiveIntegerField()
    reservation_time = models.DateTimeField()
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name="reservations"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    def __str__(self):
        return (
            f"{self.reservation_time} - {self.customer_name} ({self.num_guests} guests)"
        )