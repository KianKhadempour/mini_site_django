import datetime as dt
import enum
from calendar import JUNE, SEPTEMBER

from django.db import models
from django.urls import reverse
from django.utils import timezone


class TeamManager(models.Manager):
    def point_total_histories(self):
        return [list(team.point_total_history().values()) for team in self.all()]


class Month(enum.StrEnum):
    SEPTEMBER = "September"
    OCTOBER = "October"
    NOVEMBER = "November"
    DECEMBER = "December"
    JANUARY = "January"
    FEBRUARY = "February"
    MARCH = "March"
    APRIL = "April"
    MAY = "May"
    JUNE = "June"

    def previous(self):
        match self:
            case Month.OCTOBER:
                return Month.SEPTEMBER
            case Month.NOVEMBER:
                return Month.OCTOBER
            case Month.DECEMBER:
                return Month.NOVEMBER
            case Month.JANUARY:
                return Month.DECEMBER
            case Month.FEBRUARY:
                return Month.JANUARY
            case Month.MARCH:
                return Month.FEBRUARY
            case Month.APRIL:
                return Month.MARCH
            case Month.MAY:
                return Month.APRIL
            case Month.JUNE:
                return Month.MAY
            case _:
                raise NotImplementedError("No previous month for September")

    @classmethod
    def all(cls):
        return [
            Month.SEPTEMBER,
            Month.OCTOBER,
            Month.NOVEMBER,
            Month.DECEMBER,
            Month.JANUARY,
            Month.FEBRUARY,
            Month.MARCH,
            Month.APRIL,
            Month.MAY,
            Month.JUNE,
        ]

    def __repr__(self) -> str:
        return self.value


class Team(models.Model):
    name = models.CharField(max_length=127)

    objects = TeamManager()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Team(name="{self.name}", points={self.points()})'

    def get_absolute_url(self):
        return reverse("teams:team_detail", args=[self.pk])

    def points(self):
        return sum(
            event.points
            for event in PointEvent.current_school_year_objects.filter(team=self)
        )

    def point_total_history(self) -> dict[str, int]:
        total = 0
        ret = {
            Month.SEPTEMBER: 0,
            Month.OCTOBER: None,
            Month.NOVEMBER: None,
            Month.DECEMBER: None,
            Month.JANUARY: None,
            Month.FEBRUARY: None,
            Month.MARCH: None,
            Month.APRIL: None,
            Month.MAY: None,
            Month.JUNE: None,
        }

        for event in PointEvent.current_school_year_objects.filter(team=self).order_by(
            "created_at"
        ):
            total += event.points
            month = Month(event.created_at.strftime("%B"))
            ret.update({month: total})

        for month in Month.all()[1:]:
            if ret[month] is None:
                ret[month] = ret[month.previous()]

        return ret


class Student(models.Model):
    class Grade(models.IntegerChoices):
        GRADE_8 = 8
        GRADE_9 = 9
        GRADE_10 = 10
        GRADE_11 = 11
        GRADE_12 = 12

    team = models.ForeignKey(Team, on_delete=models.RESTRICT)
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    grade = models.IntegerField(choices=Grade)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.grade})"

    def __repr__(self):
        return f'Student(team="{self.team}", first_name="{self.first_name}", last_name="{self.last_name}", grade={self.grade})'


class CurrentSchoolYearManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        start_date = timezone.make_aware(
            dt.datetime(
                now.year if now.month >= SEPTEMBER else now.year - 1, SEPTEMBER, 1
            )
        )
        end_date = timezone.make_aware(dt.datetime(start_date.year + 1, JUNE, 30))
        return (
            super()
            .get_queryset()
            .filter(created_at__gte=start_date, created_at__lt=end_date)
        )


def truncate(s, length=20):
    if len(s) > length:
        return s[:length] + "..."
    return s


class PointEvent(models.Model):
    team = models.ForeignKey(Team, on_delete=models.RESTRICT)
    points = models.IntegerField()
    name = models.CharField(max_length=127)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=True)

    objects = models.Manager()
    current_school_year_objects = CurrentSchoolYearManager()

    def __str__(self):
        return f"{self.name} ({self.team} {self.points})"

    def __repr__(self):
        return f"PointEvent(team={self.team}, points={self.points}, name={self.name}, description={truncate(self.description)}, created_at={self.created_at})"
