from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    # User views
    path("", views.UserList.as_view(), name="user_list"),
    path("<uuid:pk>/trips/", views.UserTrips.as_view(), name="user_trips"),
]
