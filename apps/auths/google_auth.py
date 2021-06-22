from apps.auths.users_views import UsersViewSet
import google_auth_oauthlib.flow
from google.oauth2 import id_token
from google.auth.transport import Response, requests
import json
import jwt

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


def get_jwt(credentials):
    google_request = requests.Request()
    decoded_user_data = id_token.verify_oauth2_token(
        credentials.id_token, google_request
    )

    userData = dict()
    userData["sub"] = decoded_user_data["sub"]
    userData["email"] = decoded_user_data["email"]
    userData["name"] = decoded_user_data["name"]
    userData["picture"] = decoded_user_data["picture"]

    find_user = UsersViewSet().get(userData["sub"])

    if len(find_user) == 1:
        token = jwt.encode(
            {"sub": userData["sub"]}, "temporalSecret", algorithm="HS256"
        )
        return token
    else:
        UsersViewSet().create(userData)
        token = jwt.encode(
            {"sub": userData["sub"]}, "temporalSecret", algorithm="HS256"
        )
        return token

    # print("sub", decoded_user_data["sub"])
    # print("email", decoded_user_data["email"])
    # print("name", decoded_user_data["name"])
    # print("picture", decoded_user_data["picture"])
