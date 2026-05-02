from django.contrib import admin

from .models import BookingReservation


@admin.register(BookingReservation)
class BookingReservationAdmin(admin.ModelAdmin):
    list_display = (
        "reference_code",
        "full_name",
        "organization",
        "attendance_type",
        "guest_count",
        "status",
        "created_at",
    )
    search_fields = (
        "reference_code",
        "full_name",
        "email",
        "phone",
        "organization",
        "role_title",
    )
    list_filter = ("status", "attendance_type", "guest_count", "created_at")
    readonly_fields = ("reference_code", "created_at")
    ordering = ("-created_at",)
    list_per_page = 25
    actions = ("mark_confirmed", "mark_waitlist")

    fieldsets = (
        (
            "Attendee",
            {
                "fields": (
                    "reference_code",
                    "full_name",
                    "email",
                    "phone",
                    "organization",
                    "role_title",
                    "attendance_type",
                )
            },
        ),
        (
            "Application",
            {
                "fields": (
                    "guest_count",
                    "goals",
                    "status",
                    "created_at",
                )
            },
        ),
    )

    @admin.action(description="Mark selected reservations as confirmed")
    def mark_confirmed(self, request, queryset):
        queryset.update(status=BookingReservation.Status.CONFIRMED)

    @admin.action(description="Mark selected reservations as waitlist")
    def mark_waitlist(self, request, queryset):
        queryset.update(status=BookingReservation.Status.WAITLIST)


admin.site.site_header = "UWork Summit Admin"
admin.site.site_title = "UWork Summit"
admin.site.index_title = "Applications and attendee operations"
