from rest_framework import serializers, viewsets
from apps.auths.models import User
from apps.auths.serializers import UserSerializer


class UsersViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = UserSerializer

    def get(self, sub):
        return User.objects.filter(sub=sub)

    def create(self, request):
        serializer = self.serializer_class(data=request)
        if serializer.is_valid():
            serializer.save()
            return {"message": "User created"}
