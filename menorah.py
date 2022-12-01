# TODO: reformat
# TODO: add click and parameterize options
# TODO: spec out how to add and pick patterns
# TODO: make a streamlit UI

import os
import sys
import time
from random import randint, choice 
from datetime import date, timedelta, datetime

start_date = datetime.strptime("2022-12-18", "%Y-%m-%d").date()
chanukah_dates = [start_date + timedelta(days=i) for i in range(8)]


class Colors:

    def __init__(self, colors):
        self.current = 0
        self.colors = colors

    def get_random(self):
        return choice(self.colors)

    def get_next(self):
        color = self.colors[self.current]
        self.current = ( self.current + 1) % len(self.colors)
        return color

def random_color(any_color=True):
    return randint(0, 255), randint(0, 255), randint(0, 255)

class Menorah:
    def __init__(self, print_only = (os.getenv("PRINT_ONLY") == 'True')):
        if not print_only:
            import board
            import neopixel

            pixel_order = neopixel.GRB

            self.pixels = neopixel.NeoPixel(board.D18, 9, brightness=1,
                                            auto_write=False,
                                            pixel_order=pixel_order)
            self.pixel_order = pixel_order
        else:
            self.pixels = None
            self.pixel_order = "RGB"

        self.reverse = True
        self.shamash = 4
        self.print_only = print_only
    
    def _get_lights(self, night):
        assert night >= 1, "Night must be at least 1"
        assert night <= 8, "Night can't be more than 8"
    
        lights = list(range(9))
        if self.reverse:
            lights.reverse()
        lights.pop(self.shamash)
        lights = lights[-night:]
        return lights


    def _led_on(self, light, color, fade=0):
        if self.pixel_order == "GRB":
            color = (color[1], color[0], color[2])
        self.pixels[light] = color
        self.pixels.show()

    def _led_off(self, light, fade=0):
        self.pixels[light] = (0, 0, 0)
        self.pixels.show()

    def off(self, fade=0):
        for led in range(9):
            self._led_off(led, fade=fade)

    def light(self, night, color = (255, 255, 255)):
        lights = self._get_lights(night)
        self._led_on(self.shamash, color)
        for light in lights:
            self._led_on(light, color)


    # Fun patterns
    def fan_out(self, color = (255, 255, 255), delay = 0.25):
        for i in range(5):
            self._led_on(4+i, color=color)
            self._led_on(4-i, color=color)
            time.sleep(delay)
            self._led_off(4+i)
            self._led_off(4-i)

    def color_chase(self, night, color = (255, 255, 255), delay = 0.25):
        lights = [self.shamash] + self._get_lights(night)
        for light in lights:
            self._led_on(light, color)
            time.sleep(delay)

if __name__ == '__main__':
    print("Lighting the Menorah. Ctrl-C to put it out.")
    stop_time = time.time() + 60*60*4.5
    try:
        menorah = Menorah()
        rainbow_colors = Colors(
            colors = [
                (255, 0 , 0),
                (255, 127, 0),
                (255, 255, 0),
                (0, 255, 0),
                (0, 0, 255),
                (75, 0, 130),
                (148, 0, 211),
            ]        
        )
        ukraine_colors = Colors(
            colors = [(0, 87, 183), (255, 215, 0)]
        )
        israel_colors = Colors(
            colors = [(0, 56, 184), (255, 255, 255)]
        )
        today = date.today()
        while time.time() < stop_time:
            if today not in chanukah_dates:
                menorah.fan_out(color = rainbow_colors.get_next())
            else:
                night = chanukah_dates.index(today) + 1
                menorah.color_chase(night, color=ukraine_colors.get_next())
    except KeyboardInterrupt:
        menorah.off()
        print("\nPutting out the Menorah.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
