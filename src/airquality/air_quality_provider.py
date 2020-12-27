
from abc import ABC, abstractmethod

from airquality.air_quality import AirQuality


class AirQualityProvider(ABC):

    @abstractmethod
    def get_air_quality(self) -> AirQuality:
        pass
