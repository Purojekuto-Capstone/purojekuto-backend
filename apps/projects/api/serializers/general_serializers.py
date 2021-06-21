from apps.projects.models import ProjectCategory, ActivityCategory

from rest_framework import serializers

class ProjectCategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = ProjectCategory
        fields = '__all__'

class ActivityCategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = ActivityCategory
        fields = '__all__'