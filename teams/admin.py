from django.contrib import admin

from . import models


class PointEventInline(admin.TabularInline):
    model = models.PointEvent
    extra = 1


class TeamAdmin(admin.ModelAdmin):
    model = models.Team
    list_display = ("id", "name", "points")
    inlines = [PointEventInline]


class StudentAdmin(admin.ModelAdmin):
    model = models.Student
    list_display = ("id", "first_name", "last_name", "team", "grade")
    list_filter = ("team", "grade")


admin.site.register(models.Team, TeamAdmin)
admin.site.register(models.Student, StudentAdmin)
# admin.site.register(models.PointEvent)
