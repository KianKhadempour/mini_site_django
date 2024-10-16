# Generated by Django 5.1.2 on 2024-10-12 08:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_rename_score_team_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='points',
        ),
        migrations.CreateModel(
            name='PointEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField()),
                ('description', models.TextField()),
                ('event_type', models.IntegerField(choices=[(1, 'Add'), (2, 'Subtract')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='teams.team')),
            ],
        ),
    ]
