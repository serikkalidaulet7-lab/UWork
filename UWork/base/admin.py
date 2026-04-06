from django.contrib import admin

from .models import BookingReservation, UserProgress


@admin.register(BookingReservation)
class BookingReservationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "guest_count", "created_at")
    search_fields = ("full_name", "email", "phone")
    list_filter = ("guest_count", "created_at")
    readonly_fields = ("created_at",)


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'track_name',
        'sessions_completed',
        'tasks_unlocked',
        'streak',
        'tree_tokens',
        'trees_planted',
        'hero_level',
    )
