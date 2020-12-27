from abc import ABC, abstractmethod

from schedule.calendar_entry import CalendarEntry


class AbstractCalendar(ABC):

    @abstractmethod
    def get_entries(self, hours: int) -> list[CalendarEntry]:
        pass
