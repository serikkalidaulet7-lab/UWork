from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import BookingReservationForm
from .models import BookingReservation


EVENT = {
    "brand": "UWork Summit",
    "name": "UWork Future Ready Summit",
    "tagline": "A one-day summit for students, early-career builders, and hiring teams across design, product, and engineering.",
    "tagline_short": "Career strategy, product thinking, and practical networking",
    "date": "October 16, 2026",
    "date_short": "16 Oct 2026",
    "city": "Katowice, Poland",
    "venue_name": "Central Katowice district",
    "venue_note": "Exact venue packet is shared after approval.",
    "application_deadline": "October 4, 2026",
    "response_window": "2 business days",
    "capacity": 180,
    "speakers": 12,
    "tracks_label": "3 tracks",
    "start_time": "09:00",
    "closing_time": "18:30",
}

HOME_HIGHLIGHTS = [
    {
        "title": "Built for momentum",
        "copy": "Every session is designed to end with something tangible: a stronger portfolio story, a sharper job search plan, or a new collaborator.",
    },
    {
        "title": "Cross-functional by design",
        "copy": "Designers, engineers, founders, and hiring teams share the same room so the day feels closer to real product work than a lecture circuit.",
    },
    {
        "title": "Compact application flow",
        "copy": "Attendees apply with a short form, receive a reference code, and are reviewed through a clear admin workflow.",
    },
]

TRACKS = [
    {
        "title": "Product & UX",
        "format": "Case-study rooms",
        "summary": "Portfolio reviews, service design walkthroughs, and practical product thinking for people who need stronger decision-making stories.",
        "points": [
            "Presenting work beyond polished screens",
            "Turning research into narrative",
            "Showing product judgment in interviews",
        ],
    },
    {
        "title": "Engineering & AI",
        "format": "Hands-on build labs",
        "summary": "Small-group sessions focused on shipping, debugging, and explaining technical tradeoffs clearly in public and in interviews.",
        "points": [
            "Making small projects look production-aware",
            "Using AI tools without sounding generic",
            "Explaining code decisions with confidence",
        ],
    },
    {
        "title": "Career Strategy",
        "format": "Panels and mentoring",
        "summary": "Application strategy, recruiter insight, and networking structure for people who need a more deliberate path into their first serious opportunity.",
        "points": [
            "Better outreach messages and follow-up",
            "Resume positioning for early-career talent",
            "Turning side projects into proof of readiness",
        ],
    },
]

AGENDA_ITEMS = [
    {
        "time": "09:00",
        "title": "Check-in and orientation",
        "format": "Arrival",
        "description": "Badge pickup, coffee, and a fast briefing on how to move through the summit without wasting the morning in lines.",
    },
    {
        "time": "10:00",
        "title": "Opening keynote: what hiring teams notice first",
        "format": "Main stage",
        "description": "A grounded look at how junior portfolios, resumes, and side projects are actually evaluated in 2026.",
    },
    {
        "time": "11:15",
        "title": "Track sessions round one",
        "format": "Breakouts",
        "description": "Choose between product storytelling, engineering proof-of-work, or job-search strategy workshops.",
    },
    {
        "time": "13:00",
        "title": "Mentor lunch and portfolio clinics",
        "format": "Open tables",
        "description": "Short review rounds with mentors, recruiters, and peers who can give specific feedback while the day is still in motion.",
    },
    {
        "time": "14:30",
        "title": "Track sessions round two",
        "format": "Breakouts",
        "description": "A deeper working block focused on case studies, pair critiques, and sharper storytelling around real projects.",
    },
    {
        "time": "16:15",
        "title": "Hiring panel and audience Q&A",
        "format": "Panel",
        "description": "Recruiters, founders, and operators answer direct questions about applications, internships, and first full-time roles.",
    },
    {
        "time": "17:30",
        "title": "Demo showcase and close",
        "format": "Showcase",
        "description": "Attendees share progress, swap contacts, and leave with next steps rather than vague inspiration.",
    },
]

OUTCOMES = [
    "A clearer portfolio narrative for your strongest project",
    "Feedback from mentors who review real junior applications",
    "A tighter job-search plan for the next 30 days",
    "New peers working toward the same transition",
]

GUIDE_STEPS = [
    {
        "title": "Apply with context",
        "copy": "Tell us who you are, how many seats you need, and what outcome would make the day worth it for you.",
    },
    {
        "title": "Wait for review",
        "copy": "Every application is tagged with a reference code and reviewed so we can keep group size and attendee mix intentional.",
    },
    {
        "title": "Receive the venue pack",
        "copy": "Approved attendees get the exact venue packet, arrival details, and preparation notes by email.",
    },
]

POLICY_ITEMS = [
    "Keep your confirmation email and reference code ready on arrival.",
    "Respect speakers, mentors, and other attendees. Harassment or aggressive behavior ends attendance immediately.",
    "The published location is city-level only. Exact venue details are shared privately with approved guests.",
    "If your plans change, cancel early so we can release your seat to the waitlist.",
]

FAQ_ITEMS = [
    {
        "question": "Who is this event for?",
        "answer": "The program is built for students, early-career professionals, and hiring teams working across product, design, and engineering.",
    },
    {
        "question": "Do I need a finished portfolio to apply?",
        "answer": "No. A finished portfolio helps, but the sessions are structured for people who are still shaping their projects and stories.",
    },
    {
        "question": "Can I request seats for a small group?",
        "answer": "Yes. One application can request up to four seats, which works well for classmates, teammates, or community groups.",
    },
    {
        "question": "How is the venue handled?",
        "answer": "The public page only shares the city. Approved attendees receive the exact venue packet, check-in instructions, and timing details by email.",
    },
    {
        "question": "What if standard seats are gone?",
        "answer": "Applications stay open and are automatically tagged as waitlist once the active seat count reaches capacity.",
    },
]

REVIEW_FLOW = [
    "Submit an application and receive a reference code instantly.",
    "The team reviews attendee fit, seat count, and current capacity.",
    "Approved attendees receive the full venue packet and arrival checklist.",
]


def health(request):
    return HttpResponse("ok", content_type="text/plain")


def get_reservation_snapshot():
    active_reservations = BookingReservation.objects.exclude(status=BookingReservation.Status.CANCELLED)
    reserved_seats = active_reservations.aggregate(total=Sum("guest_count"))["total"] or 0
    remaining_seats = max(EVENT["capacity"] - reserved_seats, 0)

    return {
        "reserved_seats": reserved_seats,
        "remaining_seats": remaining_seats,
        "pending_review_count": active_reservations.filter(status=BookingReservation.Status.PENDING).count(),
        "confirmed_count": active_reservations.filter(status=BookingReservation.Status.CONFIRMED).count(),
        "waitlist_count": active_reservations.filter(status=BookingReservation.Status.WAITLIST).count(),
        "availability_label": "Seats available" if remaining_seats else "Waitlist open",
        "availability_note": (
            f"{remaining_seats} seats are still open for review."
            if remaining_seats
            else "Standard seats are currently full, but new applications can still join the waitlist."
        ),
    }


def build_site_context():
    snapshot = get_reservation_snapshot()

    return {
        "event": EVENT,
        "home_highlights": HOME_HIGHLIGHTS,
        "tracks": TRACKS,
        "agenda_items": AGENDA_ITEMS,
        "agenda_preview": AGENDA_ITEMS[:4],
        "outcomes": OUTCOMES,
        "guide_steps": GUIDE_STEPS,
        "policy_items": POLICY_ITEMS,
        "faq_items": FAQ_ITEMS,
        "review_flow": REVIEW_FLOW,
        "snapshot": snapshot,
        "hero_metrics": [
            {"label": "Seats remaining", "value": snapshot["remaining_seats"]},
            {"label": "Speakers", "value": EVENT["speakers"]},
            {"label": "Tracks", "value": len(TRACKS)},
        ],
    }


def guide(request):
    context = build_site_context()
    return render(request, "base/guide.html", context)


def agenda(request):
    context = build_site_context()
    return render(request, "base/agenda.html", context)


def home(request):
    if request.method == "POST":
        form = BookingReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            snapshot = get_reservation_snapshot()

            if snapshot["remaining_seats"] >= reservation.guest_count and snapshot["remaining_seats"] > 0:
                reservation.status = BookingReservation.Status.PENDING
                reservation.save()
                messages.success(
                    request,
                    f"Application received. Reference {reservation.reference_code}. We will reply within {EVENT['response_window']}.",
                )
            else:
                reservation.status = BookingReservation.Status.WAITLIST
                reservation.save()
                messages.success(
                    request,
                    f"Standard seats are full, so you have been added to the waitlist. Reference {reservation.reference_code}.",
                )
            return redirect("home")
    else:
        form = BookingReservationForm()

    context = build_site_context()
    context["form"] = form
    return render(request, "base/home.html", context)
