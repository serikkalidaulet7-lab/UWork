import re

from django import forms

from .models import BookingReservation


class BookingReservationForm(forms.ModelForm):
    full_name = forms.CharField(
        label="Full name",
        max_length=120,
        error_messages={
            "required": "Enter your full name.",
        },
    )
    phone = forms.CharField(
        label="Phone number",
        max_length=40,
        error_messages={
            "required": "Enter your phone number.",
        },
    )
    responsibility_confirmation = forms.BooleanField(
        label="I confirm that I am 18+ and accept full responsibility.",
        required=True,
        error_messages={
            "required": "You must confirm that you are 18+ and accept full responsibility.",
        },
    )

    class Meta:
        model = BookingReservation
        fields = ["full_name", "phone"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "E.g. Jan Kowalski", "autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"placeholder": "E.g. +48 123 456 789", "autocomplete": "tel"}),
        }

    def clean_full_name(self):
        full_name = " ".join(self.cleaned_data["full_name"].split())

        if len(full_name) < 2:
            raise forms.ValidationError("Full name is too short.")

        if not full_name[0].isalpha() or not full_name[0].isupper():
            raise forms.ValidationError("Full name must start with a capital letter.")

        if not re.fullmatch(r"[A-Za-zÀ-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż .'-]+", full_name):
            raise forms.ValidationError("Full name can contain only letters, spaces, apostrophes, dots, and hyphens.")

        return full_name

    def clean_phone(self):
        phone = " ".join(self.cleaned_data["phone"].split())

        if not re.fullmatch(r"[\d+\-\s()]+", phone):
            raise forms.ValidationError("Enter a valid phone number.")

        digits_only = re.sub(r"\D", "", phone)
        if not phone.startswith("+48"):
            raise forms.ValidationError("Phone number must start with +48.")

        if len(digits_only) != 11:
            raise forms.ValidationError("Enter a valid Polish phone number starting with +48.")

        return phone
