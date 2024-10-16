import pathlib
from csv import DictReader

from django.core.management.base import BaseCommand, CommandError

from teams.models import Student, Team

TEAM_IDS = [str(team.id) for team in Team.objects.all()]
GRADES = [str(grade) for grade in Student.Grade.values]


class Command(BaseCommand):
    help = "Import students from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)

    def handle(self, *args, **options):
        if (filename := options.get("filename")) is None:
            raise CommandError("No filename provided")

        file = pathlib.Path(filename)

        if not file.exists():
            raise CommandError("File does not exist")

        try:
            self.import_students(filename)
        except OSError as e:
            raise CommandError(f"Error with the file: {e}")

    def import_students(self, filename):
        with open(filename, encoding="utf-8") as f:
            if (first_line := f.readline().strip().replace(" ", "").split(",")) != [
                "team",
                "first_name",
                "last_name",
                "grade",
            ]:
                if not first_line[0].isnumeric():
                    raise CommandError(
                        f"Invalid headers. Expected: team,first_name,last_name,grade\nFound: {','.join(first_line)}"
                    )
                if first_line[0] not in TEAM_IDS:
                    raise CommandError(f"Team ID {first_line[0]} does not exist")
                if first_line[3] not in GRADES:
                    raise CommandError(
                        f"Invalid grade: {first_line[3]} (must be {', '.join(GRADES[:-1])}, or {GRADES[-1]})"
                    )

                first_line = ["team", "first_name", "last_name", "grade"]
                f.seek(0)

            csvreader = DictReader(f, fieldnames=first_line)

            if csvreader.fieldnames != ["team", "first_name", "last_name", "grade"]:
                raise CommandError(
                    "Invalid headers. Expected: team,first_name,last_name,grade\nFound: "
                    + ", ".join(csvreader.fieldnames)
                )

            for row in csvreader:
                try:
                    team = Team.objects.get(pk=row["team"])
                except Team.DoesNotExist:
                    raise CommandError(f"Team ID {row['team']} does not exist")

                if row["grade"] not in GRADES:
                    raise CommandError(
                        f"Invalid grade: {row['grade']} (must be {", ".join(GRADES[:-1])}, or {GRADES[-1]})"
                    )

                if not row["first_name"]:
                    raise CommandError("First name is required")

                if not row["last_name"]:
                    raise CommandError("Last name is required")

                student = team.student_set.create(
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    grade=row["grade"],
                )

                self.stdout.write(
                    self.style.SUCCESS(f"Created student {student} on team {team}")
                )
