
from abc import ABC, abstractmethod
import datetime
from typing import Optional

from weather.weather_forecast import WeatherForecast


class WeatherProvider(ABC):

    @abstractmethod
    def get_current_weather(self) -> WeatherForecast:
        pass

    @abstractmethod
    def get_weather(self, time: datetime.datetime) -> Optional[WeatherForecast]:
        pass
