from schedule.abstract_calendar import AbstractCalendar
from schedule.google_calendar import GoogleCalendar
from schedule.outlook_calendar import OutlookCalendar

calendars: dict = {
    "outlook": lambda config: OutlookCalendar(config),
    "google": lambda config: GoogleCalendar(config)
}


def make_provider(provider: str, config: dict) -> AbstractCalendar:
    return calendars[provider](config)
