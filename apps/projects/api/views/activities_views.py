from apps.projects.events_views import EventsAPI
from apps.auths.decode_token import decode_token

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.projects.api.serializers.activities_serializers import ActivitySerializer


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

    def get_queryset(self, activity_id=None):
        if activity_id is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return (
            self.get_serializer()
            .Meta.model.objects.filter(activity_id=activity_id)
            .first()
        )

    def list(self, request):
        token = self.verifyAuth(request)
        if token:
            activity_serializer = self.get_serializer(
                self.get_queryset(activity_id=self.request.query_params["activity_id"])
            )
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
        token = self.verifyAuth(request)
        if token:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                print(
                    "here is the serialized data", serializer.validated_data["project"]
                )
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
        token = self.verifyAuth(request)
        activity_id = self.request.query_params["activity_id"]
        if token:
            if self.get_queryset(activity_id):
                activity_serializer = self.serializer_class(
                    self.get_queryset(activity_id),
                    request.data,
                )
                if activity_serializer.is_valid():
                    updated_activity = EventsAPI().update_event(
                        token,
                        {
                            "project_id": self.request.query_params["project_id"],
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
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
