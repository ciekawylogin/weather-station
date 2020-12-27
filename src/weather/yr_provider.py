from typing import Optional, List

from yr.libyr import Yr
import datetime

from weather.weather_forecast import WeatherForecast
from weather.weather_provider import WeatherProvider
from weather.weather_summary import WeatherSummary


class YrProvider(WeatherProvider):
    refresh_period: datetime.timedelta
    location: str

    def __init__(self, config: dict):
        self.refresh_period = datetime.timedelta(minutes=config['refresh'])
        self.location = config['location']

    cached_forecasts: List[WeatherForecast] = None
    last_refresh: datetime.datetime = None

    def refresh_cache(self):
        weather = Yr(location_name=self.location)
        weather_forecast = weather.forecast(as_json=False)
        for forecast in weather_forecast:
            print (forecast)
        self.cached_forecasts = [self.convert_forecast(forecast) for forecast in weather_forecast]
        self.last_refresh = datetime.datetime.now()

    def refresh_cache_if_old(self):
        if self.last_refresh is None or datetime.datetime.now() > self.last_refresh + self.refresh_period:
            self.refresh_cache()

    @staticmethod
    def convert_summary(yr_summary) -> WeatherSummary:
        return SUMMARY_MAPPING.get(yr_summary, WeatherSummary.UNKNOWN)

    def get_current_weather(self) -> Optional[WeatherForecast]:
        self.refresh_cache_if_old()
        return self.cached_forecasts[0]

    def get_weather(self, time: datetime.datetime) -> Optional[WeatherForecast]:
        self.refresh_cache_if_old()
        for forecast in self.cached_forecasts:
            _from = forecast.from_time
            _to = forecast.to_time
            if _from <= time <= _to:
                return forecast
        return None

    @staticmethod
    def convert_forecast(dictionary: dict) -> WeatherForecast:
        weather_summary = SUMMARY_MAPPING[dictionary['symbol']['@var']]
        return WeatherForecast(
            from_time=datetime.datetime.fromisoformat(dictionary['@from']),
            to_time=datetime.datetime.fromisoformat(dictionary['@to']),
            temperature=dictionary['temperature']['@value'],
            wind_mps=dictionary['windSpeed']['@mps'],
            wind_name=dictionary['windSpeed']['@name'],
            precip_mm=dictionary['precipitation']['@value'],
            air_pressure=float(dictionary['pressure']['@value']),
            summary=weather_summary,
            precip_name=PRECIP_NAME_MAPPING[weather_summary.value]
        )


SUMMARY_MAPPING = {
    '10': WeatherSummary.HEAVY_RAIN,
    '11': WeatherSummary.THUNDER,
    '12': WeatherSummary.HEAVY_SNOW,
    '13': WeatherSummary.HEAVY_SNOW,
    '14': WeatherSummary.THUNDER,
    '15': WeatherSummary.FOG,
    '22': WeatherSummary.THUNDER,
    '23': WeatherSummary.THUNDER,
    '30': WeatherSummary.THUNDER,
    '31': WeatherSummary.THUNDER,
    '32': WeatherSummary.THUNDER,
    '33': WeatherSummary.THUNDER,
    '34': WeatherSummary.THUNDER,
    '46': WeatherSummary.LIGHT_RAIN,
    '47': WeatherSummary.LIGHT_SNOW,
    '48': WeatherSummary.HEAVY_SNOW,
    '49': WeatherSummary.LIGHT_SNOW,
    '50': WeatherSummary.HEAVY_SNOW,
    '04': WeatherSummary.CLOUDY,
    '09': WeatherSummary.HEAVY_RAIN,
    '01d': WeatherSummary.CLEAR_SKY_DAY,
    '02d': WeatherSummary.PARTLY_CLOUDY_DAY,
    '03d': WeatherSummary.PARTLY_CLOUDY_DAY,
    '40d': WeatherSummary.LIGHT_RAIN,
    '05d': WeatherSummary.HEAVY_RAIN,
    '41d': WeatherSummary.HEAVY_RAIN,
    '42d': WeatherSummary.LIGHT_SNOW,
    '07d': WeatherSummary.HEAVY_SNOW,
    '43d': WeatherSummary.HEAVY_SNOW,
    '44d': WeatherSummary.LIGHT_SNOW,
    '08d': WeatherSummary.HEAVY_SNOW,
    '45d': WeatherSummary.HEAVY_SNOW,
    '24d': WeatherSummary.THUNDER,
    '06d': WeatherSummary.THUNDER,
    '25d': WeatherSummary.THUNDER,
    '26d': WeatherSummary.THUNDER,
    '20d': WeatherSummary.THUNDER,
    '27d': WeatherSummary.THUNDER,
    '28d': WeatherSummary.THUNDER,
    '21d': WeatherSummary.THUNDER,
    '29d': WeatherSummary.THUNDER,
    '01n': WeatherSummary.CLEAR_SKY_NIGHT,
    '02n': WeatherSummary.PARTLY_CLOUDY_NIGHT,
    '03n': WeatherSummary.PARTLY_CLOUDY_NIGHT,
    '40n': WeatherSummary.LIGHT_RAIN,
    '05n': WeatherSummary.HEAVY_RAIN,
    '41n': WeatherSummary.HEAVY_RAIN,
    '42n': WeatherSummary.LIGHT_SNOW,
    '07n': WeatherSummary.HEAVY_SNOW,
    '43n': WeatherSummary.HEAVY_SNOW,
    '44n': WeatherSummary.LIGHT_SNOW,
    '08n': WeatherSummary.HEAVY_SNOW,
    '45n': WeatherSummary.HEAVY_SNOW,
    '24n': WeatherSummary.THUNDER,
    '06n': WeatherSummary.THUNDER,
    '25n': WeatherSummary.THUNDER,
    '26n': WeatherSummary.THUNDER,
    '20n': WeatherSummary.THUNDER,
    '27n': WeatherSummary.THUNDER,
    '28n': WeatherSummary.THUNDER,
    '21n': WeatherSummary.THUNDER,
    '29n': WeatherSummary.THUNDER
}

PRECIP_NAME_MAPPING = dict([
    (0, "Unknown"),
    (1, "No rain"),
    (2, "No rain"),
    (3, "No rain"),
    (4, "No rain"),
    (5, "No rain"),
    (6, "No rain"),
    (7, "Light rain"),
    (8, "Heavy rain"),
    (9, "Light snow"),
    (10, "Heavy snow"),
    (11, "Thunderstorm"),
])
