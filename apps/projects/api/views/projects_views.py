from apps.projects.utils.calendar_views import CalendarAPI
from apps.auths.utils.decode_token import decode_token
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.projects.api.serializers.projects_serializers import (
    ProjectCategorySerializer,
    ProjectSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def verifyAuth(self, request):
        if request.META.get("HTTP_AUTHORIZATION") == None:
            return False
        else:
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
        """
        Return all the projects/calendars store in the app


        params
        user ---> The id of the user.
        project_name ---> The name of the project.
        project_category ---> The id of the project category.
        start_date ---> The date the project was started.
        end_date ---> The date the project is finish.
        work_time ---> work hours in the week.
        break_time ---> break hours in the week.
        """
        token = self.verifyAuth(request)
        if token:
            project_serializer = self.get_serializer(
                self.get_queryset(project_id=self.request.query_params["project_id"])
            )
            CalendarAPI().get_calendar(token, self.request.query_params["project_id"])
            # print("aqui esta el calendar", calendar)
            return Response(project_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def create(self, request):
        """
        Create a projects/calendars


        params
        project_name ---> The name of the project.
        project_category ---> The id of the project category.
        start_date ---> The date the project was started.
        end_date ---> The date the project is finish.
        work_time ---> work hours in the week.
        break_time ---> break hours in the week.
        """
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
                    {
                        "message": "Project create succesfully",
                        "project_id": serializer.validated_data["project_id"],
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def destroy(self, request, pk=None):
        """
        Delete a project/calendar by id

        """
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

    def put(self, request):
        token = self.verifyAuth(request)
        project_id = self.request.query_params["project_id"]
        if token:
            if self.get_queryset(project_id):
                project_serializer = self.serializer_class(
                    self.get_queryset(project_id), self.request.data
                )
                if project_serializer.is_valid():
                    updated_calendar = CalendarAPI().update_calendar(
                        token, project_id, project_serializer.validated_data
                    )
                    project_serializer.validated_data["project_id"] = updated_calendar
                    project_serializer.save()
                    return Response(
                        {
                            "message": "Project updated succesfully",
                            "project_id": project_serializer.validated_data[
                                "project_id"
                            ],
                        },
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    project_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
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
        """
        Return all the projects categories store in the app


        params
        id ---> The unique id of the event.
        state ---> The state of the event (False/True).
        created_date ---> The date the event was created.
        modified_date ---> The date the event was modified.
        deleted_date ---> The date the event was deleted.
        project_category_name ---> The name of the category name.
        """
        token = self.verifyAuth(request)
        if token:
            project_serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(project_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
