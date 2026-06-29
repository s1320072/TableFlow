from django.contrib import admin

from apps.reservations.models import Reservation, Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ["table_number", "capacity", "is_active"]
    list_editable = ["is_active"]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        "customer_name",
        "num_guests",
        "reservation_time",
        "table",
        "status",
    ]
    list_filter = ["status"]
