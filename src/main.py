import sys

from yr.libyr import Yr

import subprocess
from PIL import Image
from epaper import epd7in5b_HD
import os

from drawing import draw_svg

if __name__ == "__main__":
    # weather = Yr(location_name='Netherlands/Flevoland/Almere')
    #
    # for i in weather.forecast(as_json=True):
    #     print(i)
    draw_svg.draw("example.svg")
    subprocess.run(["convert", "-size", "880x528", "-depth", "1", "example.svg", "example.bmp"])

    # open method used to open different extension image file
    im = Image.open(r"example.bmp")

    epd = epd7in5b_HD.EPD()
    # logging.info("init and Clear")
    epd.init()
    epd.Clear()

    # logging.info("3.read bmp file...")
    blackimage = Image.open(r'7in5_HD_b.bmp')
    redimage = Image.open(r'7in5_HD_b.bmp')
    epd.display(epd.getbuffer(blackimage), epd.getbuffer(redimage))
    # time.sleep(1)
