import svgwrite
from svgwrite import px


def draw_small(x: int, y: int, dwg: svgwrite.Drawing):
    shapes = dwg.add(dwg.g())

    shapes.add(dwg.rect(insert=(x, y), size=(200 * px, 200 * px),
                        fill='white', stroke='black', stroke_width=1))

    paragraph = dwg.add(dwg.g(font_size=80))
    paragraph.add(dwg.text("20°", (x+100, y+80), text_anchor="middle"))

    image = dwg.add(
        dwg.image(href=("/Users/mkrawcak/weather-station/meteocons-icons/SVG/2.svg"), insert=(10 + x, 100 + y), size=(90 * px, 90 * px)))

    pressure_text = dwg.add(dwg.g(font_size=32, font_family="Helvetica"))
    pressure_text.add(dwg.text("1023 hPa ↗", (100 + x, 120 + y)))



def draw(filename: str) -> None:
    dwg = svgwrite.Drawing(filename=filename, debug=True, size=(880 * px, 528 * px))
    bg = dwg.add(dwg.g(id='bg'))
    bg.add(dwg.rect(insert=(0 * px, 0 * px), size=(880 * px, 528 * px),
                    fill='white', stroke_width=0))

    shapes = dwg.add(dwg.g(id='shapes'))

    shapes.add(dwg.rect(insert=(20 * px, 20 * px), size=(360 * px, 290 * px),
                        fill='white', stroke='black', stroke_width=1))

    paragraph = dwg.add(dwg.g(font_size=120))
    paragraph.add(dwg.text("20°", (260, 130), text_anchor="middle"))

    image = dwg.add(
        dwg.image(href=("/Users/mkrawcak/weather-station/meteocons-icons/SVG/2.svg"), insert=(20 * px, 20 * px), size=(130 * px, 130 * px)))
    # image_border_DEBUG = dwg.add(dwg.rect(insert=(30*px, 30*px), size=(120*px, 120*px), fill="none", stroke='black', stroke_width=1))

    feels_like_text = dwg.add(dwg.g(font_size=36, font_family="Helvetica"))
    feels_like_text.add(dwg.text("Feels like 19℃", (30, 190)))

    wind_text = dwg.add(dwg.g(font_size=36, font_family="Helvetica"))
    wind_text.add(dwg.text("Wind: 2 m/s", (30, 225)))

    precipation_text = dwg.add(dwg.g(font_size=36, font_family="Helvetica"))
    precipation_text.add(dwg.text("Precipation: 2 mm", (30, 260)))

    pressure_text = dwg.add(dwg.g(font_size=36, font_family="Helvetica"))
    pressure_text.add(dwg.text("1020 hPa ↗", (30, 295)))

    draw_small(400, 20, dwg)

    dwg.save()
