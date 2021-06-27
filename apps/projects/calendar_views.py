# In all flows, verify that the project belongs to the user
import json
from apps.auths.users_views import UsersView
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class CalendarAPI:
    def prepare_credentials(self, token):

        credentials_json = json.loads(
            UsersView().get(sub=token["sub"]).values_list("credentials")[0][0]
        )
        credentials = Credentials(
            token=credentials_json["token"],
            refresh_token=credentials_json["refresh_token"],
            token_uri=credentials_json["token_uri"],
            client_id=credentials_json["client_id"],
            client_secret=credentials_json["client_secret"],
            scopes=credentials_json["scopes"],
        )

        return credentials

    def add_calendar(self, token, body):

        credentials = self.prepare_credentials(token)

        service = build("calendar", "v3", credentials=credentials)
        # Verify that the project name is not taken already in the db
        calendar = {
            "summary": body["project_name"],
        }
        created_calendar = service.calendars().insert(body=calendar).execute()
        calendar_id = created_calendar["id"]

        return calendar_id

    def get_calendar(self, credentials, body):

        service = build("calendar", "v3", credentials=credentials)
        calendar = service.calendars().get(calendarId=body["project_id"]).execute()

        return calendar

    def update_calendar(self, credentials, body):

        service = build("calendar", "v3", credentials=credentials)
        calendar = service.calendars().get(calendarId=body["project_id"]).execute()
        updated_calendar = (
            service.calendars()
            .update(calendarId=calendar["id"], body=body["project_name"])
            .execute()
        )

        return updated_calendar["etag"]
