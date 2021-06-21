from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.projects.api.serializers.activities_serializers import *

class ActivityViewSet(viewsets.ModelViewSet):
    serializers_class = ActivitySerializer

    def get_queryset(self):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()

    def list(self, request):
        activity_serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(activity_serializer.data, status = status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Activity create succesfully'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk = None):
        activity = self.get_queryset().filter(id = pk).first()
        if activity:
            activity.state = False
            activity.save()
            return Response({'message': 'Activity delete succesfully'}, status = status.HTTP_200_OK)
        return Response({'error': 'The Activity not found'}, status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk = None):
        if self.get_queryset(pk):
            activity_serializer = self.serializer_class(self.get_queryset(pk), request.data)
            if activity_serializer.is_valid():
                activity_serializer.save()
                return Response(activity_serializer.data, status = status.HTTP_200_OK)
            return Response(activity_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
