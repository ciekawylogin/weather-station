import asyncio
from pyairvisual import CloudAPI

from airquality.air_quality import AirQuality


class AirvisualProvider:

    def __init__(self, config: dict):
        self.api_key = config['api-key']
        self.latitude = config['latitude']
        self.longitude = config['longitude']

    @staticmethod
    def convert_aqi(aqi: int) -> AirQuality:
        if aqi < 50:
            return AirQuality.GOOD
        elif aqi < 100:
            return AirQuality.MODERATE
        elif aqi < 150:
            return AirQuality.UNHEALTHY_FOR_SENSITIVE_GROUPS
        elif aqi < 200:
            return AirQuality.UNHEALTHY
        elif aqi < 300:
            return AirQuality.VERY_UNHEALTHY
        else:
            return AirQuality.HAZARDOUS

    def get_air_quality(self) -> AirQuality:
        return asyncio.run(self._async_get_air_quality())

    async def _async_get_air_quality(self) -> AirQuality:
        cloud_api = CloudAPI(self.api_key)

        # ...or get it explicitly:
        data = await cloud_api.air_quality.nearest_city(
            latitude=self.latitude,
            longitude=self.longitude
        )
        aqi = data['current']['pollution']['aqius']
        return self.convert_aqi(aqi)


if __name__ == "__main__":
    print(asyncio.run(AirvisualProvider().get_air_quality()))
