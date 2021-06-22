from django.http import HttpResponseRedirect
from httplib2.error import ProxiesUnavailableError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from purojekutoBackend.settings import env_variables
from apps.auths.google_auth import get_auth_url, get_credentials

import google.oauth2.credentials
from googleapiclient.discovery import build
from google.oauth2 import id_token
from google.auth.transport import requests
import google_auth_oauthlib.flow
import jwt
import base64
import json


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

    # google_request = requests.Request()
    # decoded_user_data = id_token.verify_oauth2_token(
    #     credentials.id_token, google_request
    # )

    # print("sub", decoded_user_data["sub"])
    # print("email", decoded_user_data["email"])
    # print("name", decoded_user_data["name"])
    # print("picture", decoded_user_data["picture"])

    # print(decoded_user_data)
    # token = jwt.encode({"token": "thisisthetoken"}, "temporalsecret", algorithm="HS256")

    return HttpResponseRedirect(f"{env_variables.CLIENT_URL}/redirect/")
