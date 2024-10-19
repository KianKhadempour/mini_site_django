import datetime as dt

from django.http import JsonResponse

from .models import Team

MONTHS_SINCE_SEPTEMBER = (dt.datetime.now().month - 8) % 12
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


def hex_to_rgba(hex_color, alpha=None):
    hex_color = hex_color.lstrip("#")
    return (
        ("rgba" if alpha is not None else "rgb")
        + f"({int(hex_color[:2], 16)}, {int(hex_color[2:4], 16)}, {int(hex_color[4:], 16)}"
        + (f", {alpha})" if alpha is not None else ")")
    )


def teams_chart_view(request):
    teams = Team.objects.all()
    data = {
        "labels": MONTHS,
        "datasets": [
            {
                "name": team.name,
                "label": team.name,
                "data": list(team.point_total_history().values()),
                "backgroundColor": hex_to_rgba(team.color, 0.5),
                "borderColor": hex_to_rgba(team.color),
                "pointBackgroundColor": hex_to_rgba(team.color),
                "pointBorderColor": "#fff",
                "borderWidth": 1,
            }
            for team in teams
        ],
    }
    return JsonResponse(data)


def team_chart_view(request, pk):
    team = Team.objects.get(pk=pk)
    rgb = hex_to_rgba(team.color)
    data = {
        "labels": MONTHS,
        "datasets": [
            {
                "name": team.name,
                "label": team.name,
                "data": list(team.point_total_history().values()),
                "backgroundColor": hex_to_rgba(team.color, 0.5),
                "borderColor": rgb,
                "pointBackgroundColor": rgb,
                "pointBorderColor": "#fff",
                "borderWidth": 1,
            }
        ],
    }
    return JsonResponse(data)
