import pathlib
from csv import DictReader

from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_datetime

from teams.models import PointEvent, Team

TEAM_IDS = [str(team.id) for team in Team.objects.all()]


class Command(BaseCommand):
    help = "Import point events from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)

    def handle(self, *args, **options):
        if (filename := options.get("filename")) is None:
            raise CommandError("No filename provided")

        file = pathlib.Path(filename)

        if not file.exists():
            raise CommandError("File does not exist")

        try:
            self.import_point_events(filename)
        except OSError as e:
            raise CommandError(f"Error with the file: {e}")

    def import_point_events(self, filename):
        with open(filename, encoding="utf-8") as f:
            # Validate headers
            if (first_line := f.readline().strip().replace(" ", "").split(",")) != [
                "team",
                "points",
                "name",
                "description",
                "created_at",
            ]:
                raise CommandError(
                    f"Invalid headers. Expected: team_id,points,event_name,event_description,created_at\nFound: {','.join(first_line)}"
                )

            csvreader = DictReader(
                f,
                fieldnames=[
                    "team",
                    "points",
                    "name",
                    "description",
                    "created_at",
                ],
            )

            for row in csvreader:
                # Validate team ID
                try:
                    team = Team.objects.get(pk=row["team"])
                except Team.DoesNotExist:
                    raise CommandError(f"Team ID {row['team_id']} does not exist")

                # Validate points
                try:
                    points = int(row["points"])
                except ValueError:
                    raise CommandError(f"Invalid points value: {row['points']}")

                # Validate event name
                if not row["name"]:
                    raise CommandError("Event name is required")

                # Validate created_at datetime
                created_at = parse_datetime(row["created_at"])
                if created_at is None:
                    raise CommandError(
                        f"Invalid datetime format for created_at: {row['created_at']}"
                    )

                # Create PointEvent
                event = PointEvent.objects.create(
                    team=team,
                    points=points,
                    name=row["name"],
                    description=row["description"].strip(),
                    created_at=created_at,
                )

                self.stdout.write(
                    self.style.SUCCESS(f"Created point event {event} for team {team}")
                )
