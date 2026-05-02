from django.urls import path

from .views import agenda, guide, home


urlpatterns = [
    path("agenda/", agenda, name="agenda"),
    path("guide/", guide, name="guide"),
    path("", home, name="home"),
]
