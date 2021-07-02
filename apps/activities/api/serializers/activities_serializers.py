from rest_framework import serializers
from apps.activities.models import Activity, ActivityCategory


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            "activity_id",
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

    def to_representation(self, instance):
        return {
            "activity_id": instance.activity_id,
            "project": instance.project if instance.project is not None else '',
            "user": instance.user if instance.user is not None else '',
            "activity_name": instance.activity_name if instance.activity_name is not None else '',
            "activity_category": instance.activity_category.activity_category_name if instance.activity_category.activity_category_name is not None else '',
            "description": instance.description if instance.description is not None else '',
            "location": instance.location if instance.location  is not None else '',
            "color_id": instance.color_id if instance.color_id is not None else '',
            "start_date": instance.start_date if instance.start_date is not None else '',
            "end_date": instance.end_date if instance.end_date is not None else '',
            }


class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = "__all__"
