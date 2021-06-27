from apps.projects.calendar_views import CalendarAPI
from apps.auths.decode_token import decode_token
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.projects.api.serializers.projects_serializers import (
    ProjectSerializer,
    ProgressSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def verifyAuth(self, request):
        if request.META.get("HTTP_AUTHORIZATION") == None:
            return False
        else:
            print("here is the token", request.META.get("HTTP_AUTHORIZATION"))
            decoded_token = decode_token(request.META.get("HTTP_AUTHORIZATION")[7:])
            if not decoded_token:
                return False
            return decoded_token

    def get_queryset(self, project_id=None):
        if project_id is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return (
            self.get_serializer()
            .Meta.model.objects.filter(project_id=project_id, state=True)
            .first()
        )

    def list(self, request):
        token = self.verifyAuth(request)
        if token:
            project_serializer = self.get_serializer(
                self.get_queryset(project_id=self.request.query_params["project_id"])
            )
            calendar = CalendarAPI().get_calendar(
                token, self.request.query_params["project_id"]
            )
            print("aqui esta el calendar", calendar)
            return Response(project_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def create(self, request):
        token = self.verifyAuth(request)
        if token:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                project_id = CalendarAPI().add_calendar(
                    token, serializer.validated_data
                )
                serializer.validated_data["project_id"] = project_id
                serializer.save()
                return Response(
                    {"message": "Project create succesfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def destroy(self, request, pk=None):
        token = self.verifyAuth(request)
        if token:
            project = self.get_queryset().filter(id=pk).first()
            if project:
                project.state = False
                project.save()
                return Response(
                    {"message": "Project delete succesfully"}, status=status.HTTP_200_OK
                )
            return Response(
                {"error": "The project not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def update(self, request, pk=None):
        token = self.verifyAuth(request)
        if token:
            if self.get_queryset(pk):
                project_serializer = self.serializer_class(
                    self.get_queryset(pk), request.data
                )
                if project_serializer.is_valid():
                    project_serializer.save()
                    return Response(project_serializer.data, status=status.HTTP_200_OK)
                return Response(
                    project_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )


class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer

    def verifyAuth(self, request):
        if request.META.get("HTTP_AUTHORIZATION") == None:
            return False
        else:
            print("here is the token", request.META.get("HTTP_AUTHORIZATION"))
            decoded_token = decode_token(request.META.get("HTTP_AUTHORIZATION")[7:])
            if not decoded_token():
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
            return Response(
                {"Error: Unavailable Function"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def create(self, request):
        return Response(
            {"Error: Unavailable Function"}, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):
        return Response(
            {"Error: Unavailable Function"}, status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):
        return Response(
            {"Error: Unavailable Function"}, status=status.HTTP_400_BAD_REQUEST
        )
