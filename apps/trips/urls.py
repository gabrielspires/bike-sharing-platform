from django.urls import path

from . import views

app_name = "trips"

urlpatterns = [
    path("", views.TripList.as_view(), name="trip_list"),
    path("categories/", views.CategoryList.as_view(), name="category_list"),
    path("<uuid:pk>/finish/", views.FinishTrip.as_view(), name="finish_trip"),
    path("start/", views.StartTrip.as_view(), name="finish_trip"),
]
