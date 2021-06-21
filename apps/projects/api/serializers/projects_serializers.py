from django.db.models import fields
from rest_framework import serializers

from apps.projects.models import Project
from apps.projects.api.serializers.general_serializers import ProjectCategory

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'