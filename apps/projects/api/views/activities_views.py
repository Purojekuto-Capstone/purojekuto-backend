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
            activity_serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(activity_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def create(self, request):
        token = self.verifyAuth(request)
        if token:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Activity create succesfully"},
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

    def update(self, request, pk=None):
        token = self.verifyAuth(request)
        if token:
            if self.get_queryset(pk):
                activity_serializer = self.serializer_class(
                    self.get_queryset(pk), request.data
                )
                if activity_serializer.is_valid():
                    activity_serializer.save()
                    return Response(activity_serializer.data, status=status.HTTP_200_OK)
                return Response(
                    activity_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
