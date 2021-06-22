from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.projects.api.serializers.projects_serializers import *

class ProjectViewSet(viewsets.ModelViewSet):
    serializers_class = ProjectSerializer

    def get_queryset(self):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()

    def list(self, request):
        project_serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(project_serializer.data, status = status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Project create succesfully'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk = None):
        project = self.get_queryset().filter(id = pk).first()
        if project:
            project.state = False
            project.save()
            return Response({'message': 'Project delete succesfully'}, status = status.HTTP_200_OK)
        return Response({'error': 'The project not found'}, status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk = None):
        if self.get_queryset(pk):
            project_serializer = self.serializer_class(self.get_queryset(pk), request.data)
            if project_serializer.is_valid():
                project_serializer.save()
                return Response(project_serializer.data, status = status.HTTP_200_OK)
            return Response(project_serializer.errors, status = status.HTTP_400_BAD_REQUEST)