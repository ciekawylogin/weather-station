import datetime
from typing import Iterable

import sys

from yr import YR

import subprocess
from PIL import Image
from epaper import epd7in5b_HD
import argparse
import yaml

from airquality.air_quality_provider import AirQualityProvider
from airquality import air_quality_providers
from drawing import draw_svg
from schedule.abstract_calendar import AbstractCalendar
from schedule import calendars
from schedule.calendar_entry import CalendarEntry
from weather.weather_provider import WeatherProvider
from weather import weather_providers


def make_weather_provider(config: dict) -> WeatherProvider:
    return weather_providers.make_provider(config['provider'], config)


def make_air_quality_provider(config: dict) -> AirQualityProvider:
    return air_quality_providers.make_provider(config['provider'], config)


def make_calendars(config: list) -> list[AbstractCalendar]:
    return [make_calendar(calendar) for calendar in config]


def make_calendar(config: dict) -> AbstractCalendar:
    return calendars.make_provider(config['type'], config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='get weather data and your calendar entries and display it on a e-ink screen')
    parser.add_argument('--config', type=str,
                        help='location of the config file, in yaml format')

    args = parser.parse_args()
    print(args.config)

    with open(args.config) as file:
        _config = yaml.load(file, Loader=yaml.FullLoader)

        print(_config)
        all_entries: list[CalendarEntry] = []
        cals = [make_calendar(cal_config) for cal_config in _config['calendars']]
        for cal in cals:
            all_entries += cal.get_entries(hours = 240)

        print(all_entries)

        weather_provider = make_weather_provider(_config['weather'])
        weather = []
        if datetime.datetime.now().hour > 16:
            tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=10)
            tomorrow_evening = (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=18)
            weather = [
                (datetime.datetime.now(), weather_provider.get_current_weather()),
                (f"{tomorrow.day}/{tomorrow.month} 10:00", weather_provider.get_weather(tomorrow)),
                (f"{tomorrow.day}/{tomorrow.month} 18:00", weather_provider.get_weather(tomorrow_evening))
                       ]
        else:
            evening = datetime.datetime.now().replace(hour=18)
            tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=10)

            weather = [
                    (datetime.datetime.now(), weather_provider.get_current_weather()),
                    ("Today 18:00", weather_provider.get_weather(evening)),
                    (f"{tomorrow.day}/{tomorrow.month} 10:00", weather_provider.get_weather(tomorrow))
                ]


        air_quality_provider = make_air_quality_provider(_config['air_quality'])

        air_quality = air_quality_provider.get_air_quality()
        print(air_quality)


    # weather = Yr(location_name='Netherlands/Flevoland/Almere')
    #
    # for i in weather.forecast(as_json=True):
    #     print(i)
    draw_svg.draw("example.svg", all_entries, weather, air_quality)
    subprocess.run(["convert", "-size", "880x528", "-depth", "1", "example.svg", "example.bmp"])

    # open method used to open different extension image file
    # im = Image.open(r"example.bmp")

    # im.show()

    epd = epd7in5b_HD.EPD()
    # logging.info("init and Clear")
    epd.init()
    epd.Clear()
    #
    # # logging.info("3.read bmp file...")
    # blackimage = Image.open(r'7in5_HD_b.bmp')
    # redimage = Image.open(r'7in5_HD_b.bmp')
    epd.display(epd.getbuffer(blackimage), epd.getbuffer(redimage))
    time.sleep(1)
