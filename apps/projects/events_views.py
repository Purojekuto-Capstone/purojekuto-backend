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
        # Verify that the project name is not taken already in the db
        event = {
            "summary": body["activity_name"],
            "start": {"dateTime": body["start_date"].isoformat()},
            "end": {"dateTime": body["end_date"].isoformat()},
        }
        created_event = (
            service.events().insert(calendarId=body["project"], body=event).execute()
        )
        print(created_event["id"])
        event_id = created_event["id"]

        return event_id

    def get_event(self, token, body):

        credentials = self.prepare_credentials(token)

        service = build("calendar", "v3", credentials=credentials)
        event = (
            service.events()
            .get(calendarId=body["project_id"], eventId=body["activity_id"])
            .execute()
        )

        parsed_event = {
            "id": event["id"],
            "status": event["status"],
            "htmlLink": event["htmlLink"],
            "created": event["created"],
            "summary": event["summary"],
            "description": event.get("description", None),
            "location": event.get("location", None),
            "colorId": event.get("colorId", None),
            "start": event["start"]["dateTime"],
            "end": event["end"]["dateTime"],
            "reminders": event["reminders"],
        }
        return parsed_event

    def update_event(self, token, ids, body):

        credentials = self.prepare_credentials(token)

        service = build("calendar", "v3", credentials=credentials)

        event = (
            service.events()
            .get(calendarId=ids["project_id"], eventId=ids["activity_id"])
            .execute()
        )

        event["summary"] = body["activity_name"]
        event["start"]["dateTime"] = body["start_date"].isoformat()
        event["end"]["dateTime"] = body["end_date"].isoformat()

        updated_event = (
            service.events()
            .update(
                calendarId=ids["project_id"], eventId=ids["activity_id"], body=event
            )
            .execute()
        )

        return updated_event["id"]
