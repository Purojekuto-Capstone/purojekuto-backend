from django.db.models import fields
from rest_framework import serializers

from apps.projects.models import Activity
from apps.projects.api.serializers.general_serializers import ActivityCategory


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            "project",
            "user",
            "activity_name",
            # "activity_category",
            "start_date",
            "end_date",
        ]
