from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

import google.oauth2.credentials
import google_auth_oauthlib.flow


@api_view(["GET"])
def test_endpoint(request):
    """
    Testing REST Framework
    """

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "client_secret.json", scopes=["https://www.googleapis.com/auth/calendar"]
    )

    flow.redirect_uri = "http://localhost:8000/checkauth"

    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )

    return HttpResponseRedirect(authorization_url)


# Make checkauth endpoint to receive state, code
