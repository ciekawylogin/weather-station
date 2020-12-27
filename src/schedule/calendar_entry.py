from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class CalendarEntry:
    start: datetime
    length: timedelta
    title: str

    def __str__(self):
        start = self.start.strftime('%H:%M')
        if self.length > timedelta(minutes=180):
            length = f"${self.length.seconds / 3600} hours"
        else:
            length = f"${self.length.seconds / 60} minutes"
        return f"${start} ${length} ${self.title}"
