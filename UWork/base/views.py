from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import BookingReservationForm


def health(request):
    return HttpResponse("ok", content_type="text/plain")


def home(request):
    if request.method == "POST":
        form = BookingReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your place request has been sent. We will keep your name on the list.")
            return redirect("home")
    else:
        form = BookingReservationForm()

    context = {
        "rules": [
            "Invite-only entry. Keep your confirmation ready at the door.",
            "Bring your own alcohol. There is no bar on site.",
            "Entrance fee is 20 zl and cash only.",
            "Respect the space, the crew, and the city. Zero tolerance for vandalism.",
            "Look after your people. Nobody leaves alone if they need help.",
            "Phones down when the energy peaks. Be present and protect everyone's privacy.",
            "No outside drama, no aggressive behavior, no exceptions.",
            "Plan your ride home before the night starts.",
        ],
        "start_time": "20:30",
        "signals": [
            "Crazy house party energy",
            "Loud music and night atmosphere",
            "Simple rules, good people, hard vibes",
        ],
        "location": "Poland, Gilowice, St. Potokiem 10C",
        "form": form,
    }
    return render(request, "base/home.html", context)
