from django.urls import path

from . import views

app_name = "stations"

urlpatterns = [
    path("", views.StationListView.as_view(), name="stations"),
]
