import datetime
import pickle
import os.path
from typing import List, Dict

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from schedule.abstract_calendar import AbstractCalendar
from schedule.calendar_entry import CalendarEntry


class GoogleCalendar(AbstractCalendar):
    # If modifying these scopes, delete the token file
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    def __init__(self, config: Dict):

        self.calendar_name = config['name']
        self.token_file = config['token-file']
        self.credentials_file = config['credentials-file']
        self.hours = config['hours']
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_file, 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_entries(self, hours: int = 24) -> List[CalendarEntry]:
        if hours is None:
            hours = self.hours
        now = datetime.datetime.utcnow()
        events_result = self.service.events().list(calendarId=self.calendar_name, timeMin=now.isoformat() + 'Z',
                                                   timeMax=(now + datetime.timedelta(hours=hours)).isoformat() + 'Z',
                                                   singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        return [self.convert_entry(item) for item in events]

    @staticmethod
    def convert_entry(entry: Dict) -> CalendarEntry:
        start_time_txt = entry['start'].get('dateTime', entry['start'].get('date'))
        start_time = datetime.datetime.fromisoformat(start_time_txt)

        end_time_txt = entry['end'].get('dateTime', entry['end'].get('date'))
        end_time = datetime.datetime.fromisoformat(end_time_txt)

        delta = end_time - start_time

        return CalendarEntry(
            title=entry['summary'],
            start=start_time,
            length=delta
        )


if __name__ == "__main__":
    print(GoogleCalendar().get_entries())
