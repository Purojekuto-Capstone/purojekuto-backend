from django.db.models import fields
from rest_framework import serializers
import datetime

from apps.projects.models import Project
from apps.projects.api.serializers.general_serializers import ProjectCategory

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['end_date']

    def to_representation(self, instance):
        today_date = datetime.date.today()
        start_date = instance.start_date
        end_date = instance.end_date
        progress = ((end_date - today_date)/(end_date - start_date)) * 100
        return {
            'project id': instance.id,
            'today': today_date,
            'start_date': start_date,
            'end_date': end_date,
            'progress': progress
        }