from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.activities.utils.events_views import EventsAPI
from apps.auths.utils.decode_token import decode_token
from apps.activities.api.serializers.activities_serializers import (
    ActivityCategorySerializer,
    ActivitySerializer,
)


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer

    def verifyAuth(self, request):
        if request.META.get("HTTP_AUTHORIZATION") == None:
            return False
        else:
            decoded_token = decode_token(request.META.get("HTTP_AUTHORIZATION")[7:])
            if not decoded_token:
                return False
            return decoded_token

    def get_queryset(self, activity_id=None, start_date=None, end_date=None):
        if activity_id is None:
            return self.get_serializer().Meta.model.objects.filter(
                start_date__range=(start_date, end_date), state=True
            )
        elif start_date is not None:
            return self.get_serializer().Meta.model.objects.filter(
                activity_id=activity_id
            )
        else:
            return (
                self.get_serializer()
                .Meta.model.objects.filter(activity_id=activity_id)
                .first()
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
        project_id = self.request.query_params.get("project_id")
        activity_id = self.request.query_params.get("activity_id")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        token = self.verifyAuth(request)
        if token:
            activity_serializer = self.get_serializer(
                self.get_queryset(
                    activity_id=activity_id,
                    start_date=start_date,
                    end_date=end_date,
                ),
                many=True,
            )
            if activity_id == None:
                events = EventsAPI().list_events(
                    token,
                    {
                        "project_id": project_id,
                        "start_date": start_date,
                        "end_date": end_date,
                    },
                )
                # events.update(activity_serializer.data)
                return Response(events, status=status.HTTP_200_OK)
            else:
                event = EventsAPI().get_event(
                    token,
                    {
                        "activity_id": self.request.query_params["activity_id"],
                        "project_id": self.request.query_params["project_id"],
                    },
                )
                event.update(activity_serializer.data)

            return Response(event, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def create(self, request):
        """
        Create the ativities/events an store in the app


        params
        activity_name ---> The name of the activity/event.
        is_recurrent ---> The event is recurrent (False/True).
        start_date ---> The date the event was started.
        end_date ---> The date the event is finish.
        activity_category ---> The category of the event/activity.
        """
        token = self.verifyAuth(request)
        if token:
            request.data["user"] = token["sub"]
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                activity_id = EventsAPI().add_event(token, serializer.validated_data)
                serializer.validated_data["activity_id"] = activity_id
                serializer.save()
                return Response(
                    {
                        "message": "Activity create succesfully",
                        "activity_id": activity_id,
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
        Delete an activity/event by id


        params
        activity_name ---> The name of the activity/event.
        is_recurrent ---> The event is recurrent (False/True).
        start_date ---> The date the event was started.
        end_date ---> The date the event is finish.
        activity_category ---> The category of the event/activity.
        """
        token = self.verifyAuth(request)
        if token:
            activity = self.get_queryset().filter(id=pk).first()
            if activity:
                activity.state = False
                activity.save()
                return Response(
                    {"message": "Activity delete succesfully"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "The Activity not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def put(self, request):
        """
        Update the ativities/events an store in the app


        params
        activity_name ---> The name of the activity/event.
        is_recurrent ---> The event is recurrent (False/True).
        start_date ---> The date the event was started.
        end_date ---> The date the event is finish.
        activity_category ---> The category of the event/activity.
        """
        token = self.verifyAuth(request)
        activity_id = self.request.query_params["activity_id"]
        if token:
            request.data["user"] = token["sub"]
            if self.get_queryset(activity_id=activity_id):
                activity_serializer = self.serializer_class(
                    self.get_queryset(activity_id=activity_id), request.data
                )
                if activity_serializer.is_valid():
                    updated_activity = EventsAPI().update_event(
                        token,
                        {
                            "project_id": activity_serializer.validated_data["project"],
                            "activity_id": activity_id,
                        },
                        activity_serializer.validated_data,
                    )
                    activity_serializer.save()
                    return Response(
                        {
                            "message": "Activity updated succesfully",
                            "activity_id": updated_activity,
                        },
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    activity_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {"message": "Activity not found"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )


class ActivityCategoryViewSet(viewsets.GenericViewSet):
    serializer_class = ActivityCategorySerializer

    def verifyAuth(self, request):
        if request.META.get("HTTP_AUTHORIZATION") == None:
            return False
        else:
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
        Return all the activities categories store in the app


        params
        id ---> The unique id of the event.
        state ---> The state of the event (False/True).
        created_date ---> The date the event was created.
        modified_date ---> The date the event was modified.
        deleted_date ---> The date the event was deleted.
        activity_category_name ---> The name of the category name.
        """
        token = self.verifyAuth(request)
        if token:
            activity_serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(activity_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
