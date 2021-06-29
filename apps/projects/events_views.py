# In all flows, verify that the project belongs to the user
import json
from apps.auths.users_views import UsersView
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class EventsAPI:
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

    def add_event(self, token, body):

        credentials = self.prepare_credentials(token)

        service = build("calendar", "v3", credentials=credentials)

        event = {
            "summary": body["project_name"],
        }
        created_event = (
            service.events().insert(calendarId=body["id"], body=event).execute()
        )
        print(created_event["id"])
        event_id = created_event["id"]

        return event_id

    def get_event(self, token, body):

        credentials = self.prepare_credentials(token)

        service = build("calendar", "v3", credentials=credentials)
        event = (
            service.events()
            .get(calendarId=body["project_id"], eventId=body["event_id"])
            .execute()
        )
        print(event["summary"])
        return event

    def update_calendar(self, credentials, body):

        service = build("calendar", "v3", credentials=credentials)
        calendar = (
            service.events()
            .get(calendarId=body["project_id"], eventId="eventId")
            .execute()
        )
        updated_calendar = (
            service.events()
            .update(
                calendarId=calendar["id"],
                eventId=event["id"],
                body=body["project_name"],
            )
            .execute()
        )

        return updated_event["updated"]
