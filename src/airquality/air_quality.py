from enum import Enum
from dataclasses import dataclass

@dataclass(frozen=True)
class AirQuality(Enum):
    GOOD = 0,
    MODERATE = 1,
    UNHEALTHY_FOR_SENSITIVE_GROUPS = 2,
    UNHEALTHY = 3,
    VERY_UNHEALTHY = 4,
    HAZARDOUS = 5

    def humanize(self):
        if self == AirQuality.GOOD:
            return "Good"
        if self == AirQuality.MODERATE:
            return "Moderate"
        if self == AirQuality.UNHEALTHY_FOR_SENSITIVE_GROUPS:
            return "Unhealthy fsg"
        if self == AirQuality.UNHEALTHY:
            return "Unhealthy"
        if self == AirQuality.VERY_UNHEALTHY:
            return "Very unhealthy"
        if self == AirQuality.HAZARDOUS:
            return "STOP BREATHING"


