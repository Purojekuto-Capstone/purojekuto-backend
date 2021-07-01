from apps.projects.utils.calendar_views import CalendarAPI
from apps.auths.utils.decode_token import decode_token
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.projects.api.serializers.metrics_serializers import (
    ProgressSerializer,
    MetricsSerializer
)

from apps.projects.utils.data_processing import clean_data

class MetricsViewSet(viewsets.ModelViewSet):
    serializer_class = MetricsSerializer

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
        Return all the ativities/events store in the app


        params
        id ---> The unique id of the event.
        state ---> The state of the event (False/True).
        created_date ---> The date the event was created.
        modified_date ---> The date the event was modified.
        deleted_date ---> The date the event was deleted.
        activity_name ---> The name of the activity/event.
        is_recurrent ---> The event is recurrent (False/True).
        start_date ---> The date the event was started.
        end_date ---> The date the event is finish.
        project ---> The id of the event in calendar.
        activity_category ---> The category of the event/activity.
        """
        token = self.verifyAuth(request)
        if token:
            project_serializer = self.get_serializer(self.get_queryset(), many=True)
            metrics = clean_data(project_serializer.data)
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )


        return Response(metrics, status=status.HTTP_200_OK)


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
        """
        Return the progress in a project

        params
        project_id ---> The id of the project.
        today ---> the current date.
        start_date ---> The date the project was started.
        end_date ---> The date the project is finish.
        progress ---> The current progress in the project.
        """
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
        """
        Function not available
        """
        return Response(
            {"Error: Unavailable Function"}, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):
        """
        Function not available
        """
        return Response(
            {"Error: Unavailable Function"}, status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):
        """
        Function not available
        """
        return Response(
            {"Error: Unavailable Function"}, status=status.HTTP_400_BAD_REQUEST
        )