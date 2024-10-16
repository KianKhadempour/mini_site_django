from django.urls import path

from . import views

app_name = "teams"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.TeamDetailView.as_view(), name="team_detail"),
]
