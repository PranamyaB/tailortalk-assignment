from __future__ import print_function
import datetime
import os
import streamlit as st

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Google Calendar API scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    creds = None

    # If a token already exists, load it
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid credentials available
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            #  Use credentials from secrets.toml
            client_config = {
                "installed": {
                    "client_id": st.secrets.google_oauth.client_id,
                    "project_id": st.secrets.google_oauth.project_id,
                    "auth_uri": st.secrets.google_oauth.auth_uri,
                    "token_uri": st.secrets.google_oauth.token_uri,
                    "auth_provider_x509_cert_url": st.secrets.google_oauth.auth_provider_cert_url,
                    "client_secret": st.secrets.google_oauth.client_secret,
                    "redirect_uris": st.secrets.google_oauth.redirect_uris
                }
            }

            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for the next run
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

# Allow running standalone for testing
if __name__ == "__main__":
    print(create_event())
