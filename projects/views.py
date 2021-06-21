from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from purojekutoBackend.settings import env_variables

import google.oauth2.credentials
from googleapiclient.discovery import build
import google_auth_oauthlib.flow
import jwt
import base64
import json


@api_view(["GET"])
def login_endpoint(request):
    """
    Logging with google to get access to its calendar
    """

    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        json.loads(env_variables.GOOGLE_CREDENTIALS),
        scopes=[
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
        ],
    )

    flow.redirect_uri = "http://localhost:8000/checkauth"

    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )

    return HttpResponseRedirect(authorization_url)


@api_view(["GET"])
def check_auth(request):
    """
    Exchanging the code received in login_endpoint to get a token to make petitions
    """

    # Passing credentials to start flow oauth auth
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        json.loads(env_variables.GOOGLE_CREDENTIALS),
        scopes=[
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
        ],
        state=request.query_params["state"],
    )
    flow.redirect_uri = "http://localhost:8000/checkauth"

    # Getting the auth token to make petitions
    flow.fetch_token(
        authorization_response=f"https://localhost:8000'{request.get_full_path()}"
    )

    # Saving the credentials
    credentials = flow.credentials

    # Starting a new service to the calendar API with the right credentials
    service = build("calendar", "v3", credentials=credentials)

    plainToken = credentials.token

    token = base64.b64encode(plainToken.encode("utf8"))

    # Getting the primary calendar to get its id
    calendar = service.calendars().get(calendarId="primary").execute()

    print("aqui esta el calendario", calendar["id"])

    # token = jwt.encode({"token": "thisisthetoken"}, "temporalsecret", algorithm="HS256")

    return HttpResponseRedirect(f"http://localhost:3000/redirect/{token}")
