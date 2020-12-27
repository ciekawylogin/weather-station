
from dataclasses import dataclass
from datetime import datetime

from weather.weather_summary import WeatherSummary


@dataclass(frozen=True)
class WeatherForecast:
    from_time: datetime
    to_time: datetime
    temperature: int
    wind_mps: int
    wind_name: str
    precip_mm: int
    precip_name: str
    air_pressure: float
    summary: WeatherSummary





