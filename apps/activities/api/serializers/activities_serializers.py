from rest_framework import serializers
from apps.activities.models import Activity, ActivityCategory


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            "project",
            "user",
            "activity_name",
            "activity_category",
            "description",
            "location",
            "color_id",
            "start_date",
            "end_date",
        ]


class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = "__all__"
