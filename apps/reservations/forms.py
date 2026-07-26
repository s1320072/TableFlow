from django import forms
from django.urls import reverse
from django.utils import timezone

from .models import Reservation, Table


class ReservationForm(forms.ModelForm):
    table = forms.ModelChoiceField(
        queryset=Table.objects.filter(is_active=True),
        empty_label="Select a table",
        label="Table",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_table",
            }
        ),
    )

    class Meta:
        model = Reservation
        fields = ["customer_name", "num_guests", "reservation_time", "table"]
        widgets = {
            "customer_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your name"}
            ),
            "num_guests": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Number of guests",
                    "hx-get": "",
                    "hx-trigger": "change changed delay:500ms",
                    "hx-target": "#id_table",
                    "hx-swap": "innerHTML",
                }
            ),
            "reservation_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "hx-get": "",
                    "hx-trigger": "change changed delay:500ms",
                    "hx-target": "#id_table",
                    "hx-swap": "innerHTML",
                },
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        partial_url = reverse("available-tables-partial")
        for field_name in ("num_guests", "reservation_time"):
            self.fields[field_name].widget.attrs["hx-get"] = partial_url

    def clean_reservation_time(self):
        reservation_time = self.cleaned_data["reservation_time"]
        if reservation_time < timezone.now():
            raise forms.ValidationError("Cannot book a reservation in the past.")
        return reservation_time

    def clean(self):
        cleaned_data = super().clean()
        num_guests = cleaned_data.get("num_guests")
        table = cleaned_data.get("table")

        if num_guests and table and num_guests > table.capacity:
            self.add_error(
                "num_guests",
                f"Table {table.table_number} can accommodate"
                f" up to {table.capacity} guests.",
            )

        reservation_time = cleaned_data.get("reservation_time")
        if table and reservation_time:
            conflicts = Reservation.objects.filter(
                table=table,
                reservation_time=reservation_time,
            )
            if self.instance.pk:
                conflicts = conflicts.exclude(pk=self.instance.pk)
            if conflicts.exists():
                raise forms.ValidationError(
                    "This table is already reserved for the selected time."
                )

        return cleaned_data
