from django.http import HttpResponseRedirect
from django.http.response import HttpResponseServerError
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from apps.auths.utils.decode_token import decode_token
from apps.auths.api.serializers import UserSerializer
from purojekutoBackend.settings import env_variables
from apps.auths.utils.google_auth import get_auth_url, get_credentials, get_jwt


@api_view(["GET"])
def login_endpoint(request):
    """
    Logging with google to get access to its calendar and user data
    """
    auth_url = get_auth_url()

    return HttpResponseRedirect(auth_url)


@api_view(["GET"])
def check_auth(request):

    """
    Exchanging the code received in login_endpoint to get the right credentials
    """
    credentials = get_credentials(request)

    try:
        token = get_jwt(credentials)
    except Exception as e:
        print("here is the error", e)
        return HttpResponseServerError()

    return HttpResponseRedirect(f"{env_variables.CLIENT_URL}/login/{token}")


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def verifyAuth(self, request):
        if request.META.get("HTTP_AUTHORIZATION") == None:
            return False
        else:
            decoded_token = decode_token(request.META.get("HTTP_AUTHORIZATION")[7:])
            if not decoded_token:
                return False
            return decoded_token

    def get_queryset(self, user_sub=None):
        return self.get_serializer().Meta.model.objects.filter(sub=user_sub).first()

    def list(self, request):
        token = self.verifyAuth(self.request)
        if token:
            project_serializer = self.get_serializer(
                self.get_queryset(user_sub=token["sub"]),
            )
            return Response(
                {
                    "name": project_serializer.data.get("name"),
                    "picture": project_serializer.data.get("picture"),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
