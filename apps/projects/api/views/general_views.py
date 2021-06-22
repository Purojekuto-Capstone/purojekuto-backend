from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.projects.api.serializers.general_serializers import *
from apps.projects.models import ProjectCategory, ActivityCategory

class ProjectCategoryViewSet(viewsets.GenericViewSet):
    serializer_class = ProjectCategorySerializer

    def get_queryset(self, pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()

    def list(self, request):
        project_serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(project_serializer.data, status = status.HTTP_200_OK)

class ActivityCategoryViewSet(viewsets.GenericViewSet):
    # model = ActivityCategory
    serializer_class = ActivityCategorySerializer

    def get_queryset(self, pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()

    def list(self, request):
        return self.get_serializer().Meta.model.objects.filter(state = True)
