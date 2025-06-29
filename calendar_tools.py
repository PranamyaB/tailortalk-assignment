# calendar_tools.py

import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
import datetime

# Google Calendar API scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Secure token-based authentication for Streamlit Cloud
def authenticate_google():
    with open(st.secrets["GOOGLE_TOKEN_PATH"], "r") as token_file:
        creds_data = json.load(token_file)
    creds = Credentials.from_authorized_user_info(creds_data)
    return creds

# Create event using Google Calendar API
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

# Optional: Test locally if needed
if __name__ == "__main__":
    create_event()
