from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os.path
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCalendarClient:
    def __init__(self, credentials_file="credentials.json"):
        """Initialize the Google Calendar client with authentication."""
        self.credentials_file = credentials_file
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Calendar API."""
        # The file token.pickle stores the user's access and refresh tokens
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                self.creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(self.creds, token)

        self.service = build("calendar", "v3", credentials=self.creds)

    def get_next_week_events(self, calendar_id="primary"):
        """
        Retrieve all events for the next week.

        Args:
            calendar_id (str): Calendar ID to query. Use 'primary' for the authenticated user's
                             primary calendar, or a specific email address for a shared calendar.
        """
        now = datetime.utcnow()
        week_later = now + timedelta(days=7)

        time_min = now.isoformat() + "Z"  # 'Z' indicates UTC time
        time_max = week_later.isoformat() + "Z"

        events_result = (
            self.service.events()  # type: ignore
            .list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])
        return events

    def create_event(
        self,
        summary,
        start_time,
        end_time,
        description=None,
        location=None,
        calendar_id="primary",
    ):
        """
        Create a new calendar event.

        Args:
            summary (str): Event title
            start_time (datetime): Event start time
            end_time (datetime): Event end time
            description (str, optional): Event description
            location (str, optional): Event location

        Returns:
            dict: Created event details
        """
        event = {
            "summary": summary,
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "UTC",
            },
        }

        if description:
            event["description"] = description

        if location:
            event["location"] = location

        created_event = (
            self.service.events().insert(calendarId=calendar_id, body=event).execute()  # type: ignore
        )

        return created_event


# Example usage
if __name__ == "__main__":
    # Initialize the client
    calendar = GoogleCalendarClient("credentials.json")

    # Get next week's events from your personal calendar
    # Replace with your personal Gmail address
    personal_calendar = "bizzoni.andre@gmail.com"
    created_event = calendar.create_event(
        summary="Meditation",
        start_time=datetime.strptime("2026-01-09 13:00", "%Y-%m-%d %H:%M"),
        end_time=datetime.strptime("2026-01-09 14:00", "%Y-%m-%d %H:%M"),
        description="Guided meditation with Paul",
        calendar_id=personal_calendar,
    )
    print(f"Event successfully created: {created_event}\n")
    events = calendar.get_next_week_events(calendar_id=personal_calendar)
    print(f"Found {len(events)} events for next week:")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(f"- {event['summary']} at {start}")
