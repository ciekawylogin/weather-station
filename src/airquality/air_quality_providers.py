from airquality.air_quality_provider import AirQualityProvider
from airquality.airvisual_provider import AirvisualProvider

air_quality_providers: dict = {
    "airvisual": lambda config: AirvisualProvider(config)
}


def make_provider(provider_name: str, config: dict) -> AirQualityProvider:
    return air_quality_providers.get(provider_name)(config)
