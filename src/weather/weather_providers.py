from weather.weather_provider import WeatherProvider
from weather.yr_provider import YrProvider

weather_providers: dict = {
    "yr": lambda config: YrProvider(config)
}


def make_provider(provider_name: str, config: dict) -> WeatherProvider:
    return weather_providers.get(provider_name)(config)
