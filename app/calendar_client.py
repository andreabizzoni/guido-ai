from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os.path
import pickle
from models.calendar_models import CalendarEventRequest, CalendarEventResponse


class CalendarClient:
    def __init__(self, credentials_file="credentials.json"):
        self.credentials_file = credentials_file
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, ["https://www.googleapis.com/auth/calendar"]
                )
                self.creds = flow.run_local_server(port=0)

            with open("token.pickle", "wb") as token:
                pickle.dump(self.creds, token)

        self.service = build("calendar", "v3", credentials=self.creds)

    def create_event(self, event: CalendarEventRequest) -> CalendarEventResponse:
        if self.service is None:
            raise Exception("Google Calendar service not initialized.")

        response = (
            self.service.events()
            .insert(
                calendarId=event.calendar_id,
                body=event.model_dump(exclude={"calendar_id"}),
            )
            .execute()
        )

        return CalendarEventResponse(**response)
