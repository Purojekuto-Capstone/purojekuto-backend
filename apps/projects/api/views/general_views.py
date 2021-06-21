from rest_framework import viewsets
from rest_framework.response import Response

from apps.projects.api.serializers.general_serializers import *
from apps.projects.models import ProjectCategory, ActivityCategory

class ProjectCategoryViewSet(viewsets.GenericViewSet):
    model = ProjectCategory
    serializer_class = ProjectCategorySerializers

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)

    def list(self, request):
        data = self.get_queryset()
        data = self.get_serializer(data,  many = True)
        return Response(data.data)

class ActivityCategoryViewSet(viewsets.GenericViewSet):
    model = ActivityCategory
    serializer_class = ActivityCategorySerializers

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)

    def list(self, request):
        data = self.get_queryset()
        data = self.get_serializer(data,  many = True)
        return Response(data.data)
