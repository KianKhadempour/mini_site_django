from django.urls import path

from . import chart_views, views

app_name = "teams"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.TeamDetailView.as_view(), name="team_detail"),
    path("chart/", chart_views.teams_chart_view, name="teams_chart"),
    path("chart/<int:pk>", chart_views.team_chart_view, name="team_chart"),
]
