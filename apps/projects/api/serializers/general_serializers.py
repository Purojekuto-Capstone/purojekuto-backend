from apps.projects.models import ProjectCategory, ActivityCategory

from rest_framework import serializers

class ProjectCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectCategory
        fields = '__all__'

class ActivityCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityCategory
        fields = '__all__'