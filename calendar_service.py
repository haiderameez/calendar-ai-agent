from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config import SCOPES

def get_calendar_service():
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    return build("calendar", "v3", credentials=creds)

def add_event_to_calendar(event_data):
    service = get_calendar_service()

    start_time = event_data["start"]
    end_time = event_data["end"]

    if "T" in start_time:
        event = {
            "summary": event_data["summary"],
            "start": {"dateTime": start_time, "timeZone": event_data.get("timeZone", "UTC")},
            "end": {"dateTime": end_time, "timeZone": event_data.get("timeZone", "UTC")},
        }
    else:  
        event = {
            "summary": event_data["summary"],
            "start": {"date": start_time},
            "end": {"date": end_time},
        }

    created_event = service.events().insert(calendarId=event_data.get("calendarId", "primary"), body=event).execute()
    return created_event.get("htmlLink")  # Return event link
