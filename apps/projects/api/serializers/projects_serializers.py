from rest_framework import serializers
import datetime

from apps.projects.models import Project, ProjectCategory


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "user",
            "project_name",
            # "project_category",
            "start_date",
            "end_date",
            "work_time",
            "break_time",
        ]


class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = "__all__"


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["end_date"]

    def to_representation(self, instance):
        today_date = datetime.date.today()
        start_date = instance.start_date
        end_date = instance.end_date
        progress = ((end_date - today_date) / (end_date - start_date)) * 100
        return {
            "project id": instance.id,
            "today": today_date,
            "start_date": start_date,
            "end_date": end_date,
            "progress": progress,
        }
