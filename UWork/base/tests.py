from django.test import TestCase
from django.urls import reverse

from .models import BookingReservation


class HomePageTests(TestCase):
    def test_home_page_renders_project_silesia_banner(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PROJECT")
        self.assertContains(response, "SILESIA")
        self.assertContains(response, "Rules of the house")

    def test_booking_can_be_submitted_without_login(self):
        response = self.client.post(
            reverse("home"),
            data={
                "full_name": "Alicja Nowak",
                "phone": "500600700",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(BookingReservation.objects.count(), 1)
        self.assertContains(response, "Your place request has been sent.")
        self.assertEqual(BookingReservation.objects.get().phone, "500600700")
