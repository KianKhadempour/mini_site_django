import datetime

from django.views import generic

from .models import Team

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


class TeamDetailView(generic.DetailView):
    model = Team
    context_object_name = "team"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = self.object.student_set.order_by(
            "-grade", "first_name", "last_name"
        )
        return context
