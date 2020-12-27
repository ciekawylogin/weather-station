from enum import Enum


class WeatherSummary(Enum):
    UNKNOWN = 0
    CLEAR_SKY_DAY = 1
    CLEAR_SKY_NIGHT = 2
    PARTLY_CLOUDY_DAY = 3
    PARTLY_CLOUDY_NIGHT = 4
    FOG = 5
    CLOUDY = 6
    LIGHT_RAIN = 7
    HEAVY_RAIN = 8
    LIGHT_SNOW = 9
    HEAVY_SNOW = 10
    THUNDER = 11
