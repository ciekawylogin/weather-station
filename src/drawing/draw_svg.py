import datetime
from typing import Iterable, Tuple

import svgwrite
from svgwrite import px
import humanize

from airquality.air_quality import AirQuality
from schedule.calendar_entry import CalendarEntry
from weather.weather_forecast import WeatherForecast


def draw_big(x: int, y: int, dwg: svgwrite.Drawing, weather: WeatherForecast, air_quality: AirQuality):
    shapes = dwg.add(dwg.g(id='shapes'))

    shapes.add(dwg.rect(insert=(x, y), size=(360 * px, 300 * px),
                        fill='white', stroke='black', stroke_width=1))

    paragraph = dwg.add(dwg.g(font_size=120))
    paragraph.add(dwg.text(f"{weather.temperature}°", (x + 240, y + 110), text_anchor="middle"))

    image = dwg.add(
        dwg.image(href=(f"/Users/mkrawcak/weather-station/icons/{weather.summary.value}.svg"), insert=(x + 5, y + 5),
                  size=(120 * px, 120 * px)))

    feels_like_text = dwg.add(dwg.g(font_size=36, font_family="Helvetica"))
    feels_like_text.add(dwg.text(f"Air quality: {air_quality}", (x + 10, y + 165)))

    wind_text = dwg.add(dwg.g(font_size=36, font_family="Helvetica"))
    wind_text.add(dwg.text(f"{weather.wind_name} {weather.wind_mps} m/s", (x + 10, y + 205), textLength=340))

    precipitation_text = dwg.add(dwg.g(font_size=36, font_family="Helvetica"))
    precipitation_text.add(dwg.text(f"{weather.precip_name} {weather.precip_mm} mm", (x + 10, y + 245)))

    pressure_text = dwg.add(dwg.g(font_size=36, font_family="Helvetica"))
    pressure_text.add(dwg.text(f"{int(weather.air_pressure)} hPa", (x + 10, y + 285)))


def draw_small(x: int, y: int, dwg: svgwrite.Drawing, time: str, weather: WeatherForecast):
    shapes = dwg.add(dwg.g())

    shapes.add(dwg.rect(insert=(x, y), size=(220 * px, 145 * px),
                        fill='white', stroke='black', stroke_width=1))

    date_text = dwg.add(dwg.g(font_size=35, font_family="Helvetica"))
    date_text.add(dwg.text(time, (10 + x, 35 + y)))

    paragraph = dwg.add(dwg.g(font_size=55))
    paragraph.add(dwg.text(f"{weather.temperature}°", (x + 135, y + 90), text_anchor="middle"))

    image = dwg.add(
        dwg.image(href=("/Users/mkrawcak/weather-station/meteocons-icons/SVG/18.svg"),
                  insert=(10 + x, 45 + y), size=(55 * px, 55 * px)))

    pressure_text = dwg.add(dwg.g(font_size=36, font_family="Helvetica"))
    pressure_text.add(dwg.text(f"{int(weather.air_pressure)} hPa", (10 + x, 130 + y)))


def draw_calendar(x: int, y: int, dwg: svgwrite.Drawing,
                  lines: Iterable[str]):
    shapes = dwg.add(dwg.g())

    shapes.add(dwg.rect(insert=(x, y), size=(460 * px, 330 * px),
                        fill='white', stroke='black', stroke_width=1))

    offset = 35
    for line in lines:
        date_text = dwg.add(dwg.g(font_size=36, font_family="Helvetica"))
        date_text.add(dwg.text(line, (10 + x, offset + y)))
        offset += 40


def draw(filename: str, entries: Iterable[CalendarEntry], weather: Iterable[Tuple[datetime.datetime, WeatherForecast]],
         quality: AirQuality) -> None:
    dwg = svgwrite.Drawing(filename=filename, debug=True, size=(880 * px, 528 * px))
    bg = dwg.add(dwg.g(id='bg'))
    bg.add(dwg.rect(insert=(0 * px, 0 * px), size=(880 * px, 528 * px),
                    fill='white', stroke_width=0))

    draw_big(20, 20, dwg, weather=weather[0][1], air_quality=quality.humanize())
    draw_small(400, 20, dwg, time=weather[1][0], weather=weather[1][1])
    draw_small(640, 20, dwg, time=weather[2][0], weather=weather[2][1])

    calendar_entries: list[str] = []
    for entry in entries[:4]:
        formatted_delta = humanize.precisedelta(entry.length).replace("and", "")  # TODO: make it more concise

        time = "Ongoing" if entry.start.replace(tzinfo=None) < datetime.datetime.now() else \
            humanize.naturaltime(entry.start.replace(tzinfo=None)) if entry.start.date() != datetime.date.today() \
                else f"{entry.start.strftime('%H:%M')}, {formatted_delta}"
        calendar_entries.append(f"{time}")
        calendar_entries.append(f"{entry.title[:24]}{'...' if len(entry.title) > 24 else ''}")

    draw_calendar(400, 180, dwg, calendar_entries)

    dwg.save()
