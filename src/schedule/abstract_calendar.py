from abc import ABC, abstractmethod
from typing import List

from schedule.calendar_entry import CalendarEntry


class AbstractCalendar(ABC):

    @abstractmethod
    def get_entries(self, hours: int) -> List[CalendarEntry]:
        pass
