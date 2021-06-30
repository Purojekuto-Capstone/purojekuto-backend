from rest_framework import serializers
import datetime

from apps.projects.models import Project, ProjectCategory
from apps.activities.models import Activity, ActivityCategory


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

class MetricsSerializer(serializers.ModelSerializer):
    project = Project()
    project_category = ProjectCategory()
    activity_category = ActivityCategory()

    class Meta:
        model = Activity
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "activity name": instance.activity_name,
            "start date": instance.start_date,
            "end date": instance.end_date,
            "activity category": instance.activity_category.activity_category_name,
            "project name": instance.project.project_name,
            }