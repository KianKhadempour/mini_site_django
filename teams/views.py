from django.http import HttpResponse
from django.views import generic

from .models import Team


def index(request):
    return HttpResponse("You are at the teams index.")


class IndexView(generic.ListView):
    model = Team
    template_name = "teams/index.html"
    context_object_name = "teams"


class TeamDetailView(generic.DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = self.object.student_set.order_by(
            "-grade", "first_name", "last_name"
        )
        context["point_events"] = self.object.pointevent_set.order_by("-created_at")
        return context
