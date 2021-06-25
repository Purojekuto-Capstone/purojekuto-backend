from django.db import InternalError
from apps.auths.models import User
from apps.auths.serializers import UserSerializer


class UsersView:
    model = User
    serializer_class = UserSerializer

    def get(self, sub):
        return self.model.objects.filter(sub=sub)

    def create(self, body):
        new_user = self.serializer_class(data=body)
        if new_user.is_valid(raise_exception=True):
            new_user.save()
            print("todo bien")
            return {"message": "User created succesfully"}

    def update(self, body, sub):
        find_user = self.get(sub)
        if len(find_user) == 1:
            find_user.update(token=body["token"], refresh_token=body["refresh_token"])
            return {"message": "User updated succesfully"}
        else:
            raise InternalError("No user was found")
