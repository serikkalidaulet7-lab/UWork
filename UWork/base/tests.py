from django.test import TestCase
from django.urls import reverse

from .models import BookingReservation


class HomePageTests(TestCase):
    def test_home_page_renders_summit_branding(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "UWork Future Ready Summit")
        self.assertContains(response, "Request a seat")
        self.assertContains(response, "Portfolio-ready event platform")

    def test_agenda_and_guide_pages_render(self):
        for url_name in ("agenda", "guide"):
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)

    def test_booking_can_be_submitted_without_login(self):
        response = self.client.post(
            reverse("home"),
            data={
                "full_name": "Alicja Nowak",
                "email": "alicja@example.com",
                "phone": "+48 500 600 700",
                "organization": "Silesian University of Technology",
                "role_title": "Architecture student",
                "attendance_type": BookingReservation.AttendanceType.STUDENT,
                "guest_count": 2,
                "goals": "I want to improve my portfolio story.",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(BookingReservation.objects.count(), 1)
        reservation = BookingReservation.objects.get()
        self.assertContains(response, "Application received.")
        self.assertEqual(reservation.status, BookingReservation.Status.PENDING)
        self.assertTrue(reservation.reference_code)
        self.assertEqual(reservation.guest_count, 2)

    def test_new_submissions_move_to_waitlist_when_capacity_is_reached(self):
        BookingReservation.objects.create(
            full_name="Capacity Holder",
            email="capacity@example.com",
            phone="+48 111 222 333",
            organization="Studio",
            role_title="Coordinator",
            attendance_type=BookingReservation.AttendanceType.COMMUNITY,
            guest_count=180,
            status=BookingReservation.Status.CONFIRMED,
        )

        response = self.client.post(
            reverse("home"),
            data={
                "full_name": "Jan Kowalski",
                "email": "jan@example.com",
                "phone": "+48 500 600 701",
                "organization": "Community",
                "role_title": "Designer",
                "attendance_type": BookingReservation.AttendanceType.EARLY_CAREER,
                "guest_count": 1,
                "goals": "Meet other designers and product teams.",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        reservation = BookingReservation.objects.exclude(full_name="Capacity Holder").get()
        self.assertEqual(reservation.status, BookingReservation.Status.WAITLIST)
        self.assertContains(response, "waitlist")
