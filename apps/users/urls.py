from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    # User views
    path("", views.UserList.as_view(), name="user_list"),
    path("trips/", views.UserTripList.as_view(), name="user_trip_list"),
]
