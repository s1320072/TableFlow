from django.db import models

class Table(models.Model):
    table_number = models.CharField(max_length=10, unique=True, verbose_name="席番号")
    capacity = models.PositiveIntegerField(verbose_name="最大収容人数")
    is_active = models.BooleanField(default=True, verbose_name="稼働状態")

    def __str__(self):
        return f"Table {self.table_number} ({self.capacity} seats)"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', '承認待ち'),
        ('CONFIRMED', '予約確定'),
        ('CANCELLED', 'キャンセル'),
    ]
    customer_name = models.CharField(max_length=100, verbose_name="顧客名")
    num_guests = models.PositiveIntegerField(verbose_name="予約人数")
    reservation_time = models.DateTimeField(verbose_name="予約日時")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="reservations", verbose_name="割り当てられた卓")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="予約ステータス")

    def __str__(self):
        return f"{self.reservation_time} - {self.customer_name} ({self.num_guests} guests)"