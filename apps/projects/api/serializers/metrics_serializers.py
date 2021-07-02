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
    class Meta:
        model = Activity
        fields = '__all__'

    def to_representation(self, instance):
        try:
            activity_name = instance.activity_category.activity_category_name
        except:
            activity_name = "otras"

        return {
            "id": instance.id if instance.id is not None else '',
            "activity name": instance.activity_name if instance.activity_name is not None else '',
            "start date": instance.start_date if instance.start_date is not None else '',
            "end date": instance.end_date if instance.end_date is not None else '',
            "activity category": activity_name,
            "project name": instance.project.project_name if instance.project.project_name  is not None else '',
            "project start": instance.project.start_date if instance.project.start_date is not None else '',
            "project finish": instance.project.end_date if instance.project.end_date is not None else '',
            "work time": instance.project.work_time if instance.project.work_time is not None else '',
            "break time": instance.project.break_time if instance.project.break_time is not None else '',
            }