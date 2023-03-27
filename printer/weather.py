#!/usr/bin/python


# Adapted script from Adafruit
# Weather forecast for Raspberry Pi w/Adafruit Mini Thermal Printer.
# Retrieves data from DarkSky.net's API, prints current conditions and
# forecasts for next two days.
# Weather example using nice bitmaps.
# Written by Adafruit Industries.  MIT license.
# Adapted and enhanced for escpos library by MrWunderbar666

# Icons taken from https://adamwhitcroft.com/climacons/
# Check out his github: https://github.com/AdamWhitcroft/climacons


from datetime import datetime
import calendar
import urllib
from urllib.request import urlopen
import json
import time
import os

from escpos import printer, image

""" Setting up the main pathing """
this_dir, this_filename = os.path.split(__file__)
GRAPHICS_PATH = os.path.join(this_dir, "graphics/climacons/")

# Adapt to your needs
printer = printer.Usb(0x1fc9, 0x2016, in_ep=0x81, out_ep=0x01)

# You can get your API Key on www.darksky.net and register a dev account.
# Technically you can use any other weather service, of course :)
API_KEY = "YOUR API KEY"

LAT = "22.345490"  # Your Location
LONG = "114.189945"  # Your Location







deg = " C"  # Degree symbol on thermal printer, need to find a better way to use a proper degree symbol


printer.print_and_feed(n=1)
printer.control("LF")
printer.set(font="a", height=2, align="center", bold=True, double_height=True)
printer.text("Weather Forecast")
printer.text("\n")
printer.set(align="center")


# Print current conditions
printer.set(font="a", height=2, align="center", bold=True, double_height=False)
printer.text("Current conditions: \n")
printer.text("\n")


# Print forecast
printer.set(font="a", height=2, align="center", bold=True, double_height=False)
printer.text("Forecast: \n")
printer.cut()
printer.control("LF")