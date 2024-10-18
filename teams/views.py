import datetime

from chartjs.views.lines import BaseLineChartView
from django.views import generic

from .models import PointEvent, Team

MONTHS_SINCE_SEPTEMBER = (datetime.datetime.now().month - 8) % 12
MONTHS = [
    "September",
    "October",
    "November",
    "December",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
][:MONTHS_SINCE_SEPTEMBER]


class IndexView(generic.ListView):
    model = Team
    template_name = "teams/index.html"
    context_object_name = "teams"


class TeamsChartView(BaseLineChartView):
    def get_labels(self):
        """Return 10 labels for the x-axis."""
        return MONTHS

    def get_providers(self):
        """Return names of datasets."""
        return list(Team.objects.values_list("name", flat=True))

    def get_data(self):
        """Return datasets to plot."""

        return Team.objects.point_total_histories()


class TeamDetailView(generic.DetailView):
    model = Team
    context_object_name = "team"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = self.object.student_set.order_by(
            "-grade", "first_name", "last_name"
        )
        print(PointEvent.current_school_year_objects.filter(team=self.object))
        context["point_events"] = PointEvent.current_school_year_objects.filter(
            team=self.object
        ).order_by("-created_at")

        print(context["point_events"])
        return context


class TeamChartView(BaseLineChartView):
    def get_labels(self):
        """Return 10 labels for the x-axis."""
        return MONTHS

    def get_providers(self):
        """Return names of datasets."""
        return [Team.objects.get(pk=self.kwargs.get("pk")).name]

    def get_data(self):
        """Return datasets to plot."""
        return [
            list(
                Team.objects.get(pk=self.kwargs.get("pk"))
                .point_total_history()
                .values()
            )
        ]
