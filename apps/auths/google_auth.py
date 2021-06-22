import google_auth_oauthlib.flow
from google.oauth2 import id_token
import json

from purojekutoBackend.settings import env_variables

scopes = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]

redirect_uri = f"{env_variables.SERVER_URL}/checkauth"


def get_auth_url():

    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        json.loads(env_variables.GOOGLE_CREDENTIALS), scopes=scopes
    )

    flow.redirect_uri = redirect_uri

    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    return authorization_url


def get_credentials(request):

    # Passing credentials to start flow oauth auth
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        json.loads(env_variables.GOOGLE_CREDENTIALS),
        scopes=scopes,
        state=request.query_params["state"],
    )
    flow.redirect_uri = redirect_uri

    # Getting the auth token to make petitions
    flow.fetch_token(
        authorization_response=f"https://localhost:8000{request.get_full_path()}"
    )

    # Saving the credentials
    credentials = flow.credentials

    return credentials
