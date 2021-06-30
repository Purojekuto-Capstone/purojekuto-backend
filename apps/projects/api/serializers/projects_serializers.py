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



