import re

from django import forms

from .models import BookingReservation


class BookingReservationForm(forms.ModelForm):
    class Meta:
        model = BookingReservation
        fields = [
            "full_name",
            "email",
            "phone",
            "organization",
            "role_title",
            "attendance_type",
            "guest_count",
            "goals",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "placeholder": "E.g. Alicja Nowak",
                    "autocomplete": "name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "E.g. +48 500 600 700",
                    "autocomplete": "tel",
                }
            ),
            "organization": forms.TextInput(
                attrs={
                    "placeholder": "University, company, or community",
                    "autocomplete": "organization",
                }
            ),
            "role_title": forms.TextInput(
                attrs={
                    "placeholder": "Student, junior designer, recruiter...",
                    "autocomplete": "organization-title",
                }
            ),
            "attendance_type": forms.Select(),
            "guest_count": forms.NumberInput(attrs={"min": 1, "max": 4}),
            "goals": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Tell us what you want to learn, build, or who you want to meet.",
                }
            ),
        }
        labels = {
            "role_title": "Role or focus area",
            "attendance_type": "Attendee profile",
            "guest_count": "Seats requested",
            "goals": "What are you hoping to get from the day?",
        }
        help_texts = {
            "guest_count": "You can request up to 4 seats in one application.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].error_messages["required"] = "Enter your first and last name."
        self.fields["email"].error_messages["required"] = "Enter your email address."
        self.fields["phone"].error_messages["required"] = "Enter your phone number."
        self.fields["guest_count"].error_messages["required"] = "Tell us how many seats you need."

    def clean_full_name(self):
        full_name = " ".join(self.cleaned_data["full_name"].split())
        parts = [part for part in full_name.split(" ") if part]

        if len(parts) < 2:
            raise forms.ValidationError("Please enter both your first and last name.")

        if not re.fullmatch(r"[A-Za-zÀ-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż .'-]+", full_name):
            raise forms.ValidationError("Full name can contain only letters, spaces, apostrophes, dots, and hyphens.")

        return full_name

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def clean_phone(self):
        phone = " ".join(self.cleaned_data["phone"].split())

        if not re.fullmatch(r"[\d+\-\s()]+", phone):
            raise forms.ValidationError("Enter a valid phone number.")

        digits_only = re.sub(r"\D", "", phone)
        if not 7 <= len(digits_only) <= 15:
            raise forms.ValidationError("Enter a valid international phone number.")

        return phone

    def clean_organization(self):
        return " ".join(self.cleaned_data["organization"].split())

    def clean_role_title(self):
        return " ".join(self.cleaned_data["role_title"].split())

    def clean_goals(self):
        return self.cleaned_data["goals"].strip()
