from django.http import HttpResponseRedirect
from django.http.response import HttpResponseServerError
from rest_framework.decorators import api_view

from purojekutoBackend.settings import env_variables
from apps.auths.google_auth import get_auth_url, get_credentials, get_jwt


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

    return HttpResponseRedirect(
        f"{env_variables.CLIENT_URL}/login/token/?token={token}"
    )
