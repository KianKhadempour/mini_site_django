from django.db import models
from django.utils import timezone


class Team(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Team({self.name}, {self.points()})"

    def points(self):
        return sum(event.points for event in self.pointevent_set.all())


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

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.grade})"

    def __repr__(self):
        return f"Student(team={self.team}, first_name={self.first_name}, last_name={self.last_name}, grade={self.grade})"


class PointEvent(models.Model):
    team = models.ForeignKey(Team, on_delete=models.RESTRICT)
    points = models.IntegerField()
    name = models.CharField(max_length=127)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=True)

    def __str__(self):
        return f"{self.name} ({self.team} {self.points})"

    def __repr__(self):
        return f"PointEvent(team={self.team}, points={self.points}, name={self.name}, description={self.description}, created_at={self.created_at})"
