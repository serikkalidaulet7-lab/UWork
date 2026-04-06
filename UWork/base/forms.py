from django import forms

from .models import BookingReservation


class BookingReservationForm(forms.ModelForm):
    class Meta:
        model = BookingReservation
        fields = ["full_name", "phone"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone or Instagram"}),
        }
