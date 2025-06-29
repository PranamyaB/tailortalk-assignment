# calendar_tools.py
import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime

def authenticate_google():
    token_info = st.secrets["google_token"]
    creds = Credentials(
        token=token_info["token"],
        refresh_token=token_info["refresh_token"],
        token_uri=token_info["token_uri"],
        client_id=token_info["client_id"],
        client_secret=token_info["client_secret"],
        scopes=token_info["scopes"]
    )
    return creds

def create_event(summary="TailorTalk Meeting", start_time=None, duration_minutes=30):
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    if not start_time:
        start_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    end_time = start_time + datetime.timedelta(minutes=duration_minutes)

    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat() + 'Z', 'timeZone': 'UTC'},
        'end': {'dateTime': end_time.isoformat() + 'Z', 'timeZone': 'UTC'},
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    event_link = created_event.get('htmlLink')
    print(f"Event created: {event_link}")
    return event_link
