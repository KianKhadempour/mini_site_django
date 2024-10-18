import datetime as dt

from django.test import TestCase
from django.utils import timezone

from . import models


class TeamModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.team_one = models.Team.objects.create(name="Team One")
        cls.team_two = models.Team.objects.create(name="Team Two")
        cls.point_events = [
            models.PointEvent.objects.create(
                team=cls.team_one,
                points=11,
                name="Event 0",
                created_at=timezone.make_aware(dt.datetime(2025, 7, 22)),
            ),
            models.PointEvent.objects.create(
                team=cls.team_one,
                points=1,
                name="Event 1",
                created_at=timezone.make_aware(dt.datetime(2025, 3, 27)),
            ),
            models.PointEvent.objects.create(
                team=cls.team_one,
                points=2,
                name="Event 2",
                created_at=timezone.make_aware(dt.datetime(2024, 9, 16)),
            ),
            models.PointEvent.objects.create(
                team=cls.team_one,
                points=3,
                name="Event 3",
                created_at=timezone.make_aware(dt.datetime(2024, 10, 11)),
            ),
            models.PointEvent.objects.create(
                team=cls.team_two,
                points=4,
                name="Event 4",
                created_at=timezone.make_aware(dt.datetime(2024, 11, 3)),
            ),
            models.PointEvent.objects.create(
                team=cls.team_two,
                points=5,
                name="Event 5",
                created_at=timezone.make_aware(dt.datetime(2024, 12, 8)),
            ),
            models.PointEvent.objects.create(
                team=cls.team_two,
                points=6,
                name="Event 6",
                created_at=timezone.make_aware(dt.datetime(2025, 1, 19)),
            ),
            models.PointEvent.objects.create(
                team=cls.team_two,
                points=7,
                name="Event 7",
                created_at=timezone.make_aware(dt.datetime(2024, 8, 14)),
            ),
        ]

    def test_team_str(self):
        self.assertEqual(str(self.team_one), "Team One")
        self.assertEqual(str(self.team_two), "Team Two")

    def test_team_repr(self):
        self.assertEqual(repr(self.team_one), "Team(name='Team One', points=6)")
        self.assertEqual(repr(self.team_two), "Team(name='Team Two', points=15)")

    def test_team_points(self):
        self.assertEqual(self.team_one.points(), 6)
        self.assertEqual(self.team_two.points(), 15)

    def test_team_get_absolute_url(self):
        self.assertEqual(self.team_one.get_absolute_url(), "/teams/1/")
        self.assertEqual(self.team_two.get_absolute_url(), "/teams/2/")

    def test_team_point_total_history(self):
        self.assertEqual(
            self.team_one.point_total_history(),
            {
                "September": 2,
                "October": 5,
                "November": 5,
                "December": 5,
                "January": 5,
                "February": 5,
                "March": 6,
                "April": 6,
                "May": 6,
                "June": 6,
            },
        )
        self.assertEqual(
            self.team_two.point_total_history(),
            {
                "September": 0,
                "October": 0,
                "November": 4,
                "December": 9,
                "January": 15,
                "February": 15,
                "March": 15,
                "April": 15,
                "May": 15,
                "June": 15,
            },
        )

    def test_team_point_histories(self):
        self.assertEqual(
            models.Team.objects.point_total_histories(),
            [[2, 5, 5, 5, 5, 5, 6, 6, 6, 6], [0, 0, 4, 9, 15, 15, 15, 15, 15, 15]],
        )


class StudentModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.team = models.Team.objects.create(name="Team One")
        cls.student = models.Student.objects.create(
            team=cls.team,
            first_name="John",
            last_name="Doe",
            grade=models.Student.Grade.GRADE_10,
        )

    def test_student_str(self):
        self.assertEqual(str(self.student), "John Doe (10)")

    def test_student_repr(self):
        self.assertEqual(
            repr(self.student),
            "Student(team='Team One', first_name='John', last_name='Doe', grade=10)",
        )

    def test_student_full_name(self):
        self.assertEqual(self.student.full_name, "John Doe")


class PointEventModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.team = models.Team.objects.create(name="Team One")
        current_year = timezone.now().year
        start_date = timezone.make_aware(dt.datetime(current_year, 9, 1))
        end_date = timezone.make_aware(dt.datetime(current_year + 1, 6, 30))
        cls.point_events = [
            models.PointEvent.objects.create(
                team=cls.team,
                points=10,
                name="Event 1",
                description="Description 1",
                created_at=timezone.make_aware(dt.datetime(2024, 9, 16)),
            ),
            models.PointEvent.objects.create(
                team=cls.team,
                points=5,
                name="Event 2",
                description="Description 2",
                created_at=start_date,
            ),
            models.PointEvent.objects.create(
                team=cls.team,
                points=15,
                name="Event 3",
                description="Description 3",
                created_at=end_date,
            ),
            models.PointEvent.objects.create(
                team=cls.team,
                points=-5,
                name="Event 4",
                description="Description 4",
                created_at=timezone.make_aware(dt.datetime(current_year, 8, 31)),
            ),
            models.PointEvent.objects.create(
                team=cls.team,
                points=8,
                name="Event 5",
                description="Description 5",
                created_at=timezone.make_aware(dt.datetime(current_year + 1, 7, 1)),
            ),
        ]

    def test_point_event_str(self):
        self.assertEqual(str(self.point_events[0]), "Event 1 (Team One 10)")
        self.assertEqual(str(self.point_events[1]), "Event 2 (Team One 5)")
        self.assertEqual(str(self.point_events[2]), "Event 3 (Team One 15)")
        self.assertEqual(str(self.point_events[3]), "Event 4 (Team One -5)")
        self.assertEqual(str(self.point_events[4]), "Event 5 (Team One 8)")

    def test_point_event_repr(self):
        self.maxDiff = None
        self.assertEqual(
            repr(self.point_events[0]),
            "PointEvent(team='Team One', points=10, name='Event 1', description='Description 1', created_at=datetime.datetime(2024, 9, 16, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='America/Vancouver')))",
        )
        self.assertEqual(
            repr(self.point_events[1]),
            "PointEvent(team='Team One', points=5, name='Event 2', description='Description 2', created_at=datetime.datetime(2024, 9, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='America/Vancouver')))",
        )
        self.assertEqual(
            repr(self.point_events[2]),
            "PointEvent(team='Team One', points=15, name='Event 3', description='Description 3', created_at=datetime.datetime(2025, 6, 30, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='America/Vancouver')))",
        )
        self.assertEqual(
            repr(self.point_events[3]),
            "PointEvent(team='Team One', points=-5, name='Event 4', description='Description 4', created_at=datetime.datetime(2024, 8, 31, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='America/Vancouver')))",
        )
        self.assertEqual(
            repr(self.point_events[4]),
            "PointEvent(team='Team One', points=8, name='Event 5', description='Description 5', created_at=datetime.datetime(2025, 7, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='America/Vancouver')))",
        )

    def test_current_school_year_objects_manager(self):
        self.assertEqual(models.PointEvent.current_school_year_objects.count(), 3)
