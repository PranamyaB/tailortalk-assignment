# calendar_tools.py
from __future__ import print_function
import datetime
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
SCOPES = ['https://www.googleapis.com/auth/calendar']
def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
def create_event(summary="TailorTalk Meeting", start_time=None, duration_minutes=30):
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    if not start_time:
        start_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    end_time = start_time + datetime.timedelta(minutes=duration_minutes)

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
    }
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    event_link = created_event.get('htmlLink')
    print(f"Event created: {event_link}")
    return event_link
if __name__ == "__main__":
    create_event()
