from typing import Dict, List

from O365 import Account, MSGraphProtocol, calendar, FileSystemTokenBackend
import datetime

from schedule.abstract_calendar import AbstractCalendar
from schedule.calendar_entry import CalendarEntry


class OutlookCalendar(AbstractCalendar):
    client_id: str = None
    secret_id: str = None

    def __init__(self, config: Dict):
        self.client_id = config['client-id']
        self.secret_id = config['secret-id']
        self.calendar_name = config['name']
        self.token_file = config['token-file']
        self.hours = config['hours']
        credentials = (self.client_id, self.secret_id)
        protocol = MSGraphProtocol()
        scopes = ['User.Read', 'Calendars.Read', 'Calendars.Read.Shared', 'offline_access']
        self.account = Account(credentials, protocol=protocol, token_backend=FileSystemTokenBackend(token_path=self.token_file))
        if not self.account.is_authenticated:
            if self.account.authenticate(scopes=scopes):
                print('Authenticated!')
            else:
                print("Failed to authenticate")
        else:
            print("Skipping authentication because token already exists")

    def get_entries(self, hours: int = None) -> List[CalendarEntry]:
        if hours is None:
            hours = self.hours
        schedule = self.account.schedule()
        cal = schedule.get_calendar(calendar_name=self.calendar_name)
        if cal is None:
            calendars = [schedule.name for schedule in schedule.list_calendars()]
            raise RuntimeError(f"Calendar '{self.calendar_name}' does not exist for current Outlook account. Avaiblable calendars are: {calendars}")
        q = cal.new_query('start').greater_equal(datetime.datetime.now())
        q.chain('and').on_attribute('end').less_equal(datetime.datetime.now() + datetime.timedelta(hours=hours))
        events = cal.get_events(query=q, include_recurring=True)
        return [self.convert_entry(entry) for entry in events]

    @staticmethod
    def convert_entry(event: calendar.Event):
        return CalendarEntry(
            start=event.start,
            length=event.end - event.start,
            title=event.subject
        )


if __name__ == "__main__":
    print(OutlookCalendar(config={
        "client-id": "f8fa701f-6ea8-4279-8c28-820d8a5042be",
        "secret-id": "8PNh67tx_~zGTL68c_2__PC53u1H3y__wZ",
        "name": "ebay",
        "token-file": "/Users/mkrawcak/weather-station/src/o365_token.txt"
    }).get_entries())
