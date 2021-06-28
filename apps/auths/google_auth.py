from apps.auths.users_views import UsersView
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
        access_type="offline", include_granted_scopes="true", prompt="consent"
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
        authorization_response=f"{env_variables.AUTH_RESPONSE_URL}{request.get_full_path()}"
    )

    # Saving the credentials
    credentials = flow.credentials

    return credentials


def get_jwt(credentials):

    print("token", credentials.token)
    print("refreshToken", credentials.refresh_token)

    google_request = requests.Request()
    decoded_user_data = id_token.verify_oauth2_token(
        credentials.id_token, google_request
    )

    user_data = dict()
    user_data["sub"] = decoded_user_data["sub"]
    user_data["email"] = decoded_user_data["email"]
    user_data["name"] = decoded_user_data["name"]
    user_data["picture"] = decoded_user_data["picture"]
    user_data["credentials"] = credentials.to_json()

    find_user = UsersView().get(user_data["sub"])

    if len(find_user) == 1:
        UsersView().update(body=user_data, sub=user_data["sub"])
        token = jwt.encode(
            {"sub": user_data["sub"]}, "temporalSecret", algorithm="HS256"
        )
        return token
    else:
        UsersView().create(user_data)
        token = jwt.encode(
            {"sub": user_data["sub"]}, "temporalSecret", algorithm="HS256"
        )
        return token
