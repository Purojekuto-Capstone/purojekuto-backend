from rest_framework import serializers
import datetime

from apps.projects.models import Project, ProjectCategory


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "user_sub",
            "project_name",
            "project_id",
            "project_category",
            "start_date",
            "end_date",
            "work_time",
            "break_time",
        ]

    def to_representation(self, instance):
        try:
            category_name = instance.project_category.project_category_name
        except:
            category_name = "otras"

        return {
            "user_sub": instance.user_sub if instance.user_sub is not None else '',
            "project_name": instance.project_name if instance.project_name is not None else '',
            "project_id": instance.project_id if instance.project_id is not None else '',
            "project_category": category_name,
            "start_date": instance.start_date if instance.start_date is not None else '',
            "end_date": instance.end_date if instance.end_date  is not None else '',
            "work_time": instance.work_time if instance.work_time is not None else '',
            "break_time": instance.break_time if instance.break_time is not None else '',
            }

class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = "__all__"



