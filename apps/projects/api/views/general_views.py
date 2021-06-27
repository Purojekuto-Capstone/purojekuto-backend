from apps.auths.decode_token import decode_token
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.projects.api.serializers.general_serializers import (
    ProjectCategorySerializer,
    ActivityCategorySerializer,
)


class ProjectCategoryViewSet(viewsets.GenericViewSet):
    serializer_class = ProjectCategorySerializer

    def verifyAuth(self, request):
        if request.META.get("HTTP_AUTHORIZATION") == None:
            return False
        else:
            print("here is the token", request.META.get("HTTP_AUTHORIZATION"))
            decoded_token = decode_token(request.META.get("HTTP_AUTHORIZATION")[7:])
            if not decoded_token:
                return False
            return decoded_token

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return (
            self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
        )

    def list(self, request):
        token = self.verifyAuth(request)
        if token:
            project_serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(project_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )


class ActivityCategoryViewSet(viewsets.GenericViewSet):
    serializer_class = ActivityCategorySerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return (
            self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
        )

    def list(self, request):
        token = self.verifyAuth(request)
        if token:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
