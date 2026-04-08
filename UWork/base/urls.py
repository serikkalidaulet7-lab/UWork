from django.urls import path

from .views import health, home, rules


urlpatterns = [
    path("health/", health, name="health"),
    path("rules/", rules, name="rules"),
    path("", home, name="home"),
]
