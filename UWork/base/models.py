import secrets

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class BookingReservation(models.Model):
    class AttendanceType(models.TextChoices):
        STUDENT = "student", "Student"
        EARLY_CAREER = "early-career", "Early-career professional"
        HIRING_PARTNER = "hiring-partner", "Hiring partner"
        COMMUNITY = "community", "Community member"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending review"
        CONFIRMED = "confirmed", "Confirmed"
        WAITLIST = "waitlist", "Waitlist"
        CANCELLED = "cancelled", "Cancelled"

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    organization = models.CharField(max_length=120, blank=True)
    role_title = models.CharField(max_length=120, blank=True)
    attendance_type = models.CharField(
        max_length=32,
        choices=AttendanceType.choices,
        default=AttendanceType.STUDENT,
    )
    guest_count = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
    )
    goals = models.TextField(blank=True)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
    )
    reference_code = models.CharField(
        max_length=16,
        unique=True,
        null=True,
        blank=True,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.reference_code or 'draft'})"

    def save(self, *args, **kwargs):
        if not self.reference_code:
            self.reference_code = self.generate_reference_code()
        super().save(*args, **kwargs)

    @classmethod
    def generate_reference_code(cls):
        while True:
            candidate = f"UWS-{secrets.token_hex(3).upper()}"
            if not cls.objects.filter(reference_code=candidate).exists():
                return candidate
