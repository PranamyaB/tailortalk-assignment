# calendar_tools.py
from __future__ import print_function
import datetime
import os.path
import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these SCOPES, delete token.json before re-auth
SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate_google():
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": st.secrets["google_oauth"]["client_id"],
                "project_id": st.secrets["google_oauth"]["project_id"],
                "auth_uri": st.secrets["google_oauth"]["auth_uri"],
                "token_uri": st.secrets["google_oauth"]["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["google_oauth"]["auth_provider_cert_url"],
                "client_secret": st.secrets["google_oauth"]["client_secret"],
                "redirect_uris": st.secrets["google_oauth"]["redirect_uris"]
            }
        },
        SCOPES
    )
    creds = flow.run_console()
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
    print(f"Event created: {created_event.get('htmlLink')}")
    return created_event.get('htmlLink')


# Test when run standalone
if __name__ == "__main__":
    create_event()
