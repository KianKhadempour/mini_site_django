# Generated by Django 5.1.2 on 2024-10-12 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_remove_team_points_pointevent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pointevent',
            name='event_type',
        ),
        migrations.AddField(
            model_name='pointevent',
            name='name',
            field=models.CharField(default='default', max_length=127),
            preserve_default=False,
        ),
    ]
