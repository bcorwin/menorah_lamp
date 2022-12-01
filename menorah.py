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

    def get_next(self, num=1):
        colors = []
        for i in range(num):
            color = self.colors[self.current]
            self.current = (self.current + 1) % len(self.colors)
            colors.append(color)
        if num == 1:
            colors = colors[0]
        return colors


def random_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


class Menorah:
    def __init__(self, print_only=False):
        if not print_only:
            import board
            import neopixel

            pixel_order = neopixel.GRB

            self.pixels = neopixel.NeoPixel(board.D18, 9, brightness=1,
                                            auto_write=False,
                                            pixel_order=pixel_order)
            self.pixel_order = pixel_order
            self.pixels.show()
        else:
            self.pixels = 9*[(0, 0, 0)]
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
        lights = [self.shamash] + lights
        return lights

    def _led_on(self, led, color):
        if not self.print_only:
            if self.pixel_order == "GRB":
                color = (color[1], color[0], color[2])
            self.pixels[led] = color
            self.pixels.show()
        else:
            print(f"{led} set to {color}")

    def _led_off(self, led):
        self._led_on(led, (0, 0, 0))

    def _fade(self, lights, colors, fade_time, num_steps=100):
        start = [self.pixels[i] for i in lights]
        if self.pixel_order == "GRB":
            start = [(c[1], c[0], c[2]) for c in start]
        intervals = [[(y[1] - y[0]) / num_steps for y in zip(x[0], x[1])] for x in zip(start, colors)]
        steps = []
        for i in range(num_steps + 1):
            step = [(round(x[0][0] + i*x[1][0]), round(x[0][1] + i*x[1][1]), round(x[0][2] + i*x[1][2]))
                    for x in zip(start, intervals)]
            steps.append(step)

        for step in steps:
            time.sleep(fade_time / (num_steps + 1))
            for i in range(len(lights)):
                self._led_on(lights[i], step[i])

    def _lights_on(self, lights, colors, fade=0):
        assert isinstance(lights, list), "Lights must be a list"
        assert isinstance(colors, list), "Colors must be a list"
        if len(colors) == 1:
            colors = len(lights)*colors
        assert len(colors) == len(lights), \
            "Length of colors and lights must match (or set colors as single string)"

        if fade <= 0:
            for i in range(len(lights)):
                self._led_on(lights[i], colors[i])
        else:
            self._fade(lights, colors, fade_time=fade)

    def _lights_off(self, lights, fade=0):
        self._lights_on(lights, len(lights)*[(0,0,0)], fade=fade)

    def off(self, fade=0):
        self._lights_off(list(range(9)), fade=fade)

    def light(self, night, color=(255, 255, 255), fade=0):
        lights = self._get_lights(night)
        self._lights_on(lights, [color], fade=fade)

    # Fun patterns
    def fan_out(self, colors=(255, 255, 255), delay=0.25, fade=0):
        if not isinstance(colors, list):
            colors = [colors]

        for i in range(5):
            color = colors[i % len(colors)]
            lights = [4+i, 4-i]
            self._lights_on(lights, [color], fade=fade)
            time.sleep(delay)
            self._lights_off(lights, fade=fade)

    def color_chase(self, night, color=(255, 255, 255), delay=0.25, fade=0):
        lights = self._get_lights(night)
        for light in lights:
            self._lights_on([light], [color], fade=fade)
            time.sleep(delay)


if __name__ == '__main__':
    print("Lighting the Menorah. Ctrl-C to put it out.")
    stop_time = time.time() + 60 * 60 * 4.5
    try:
        menorah = Menorah()
        rainbow_colors = Colors(
            colors=[
                (255, 0, 0),
                (255, 127, 0),
                (255, 255, 0),
                (0, 255, 0),
                (0, 0, 255),
                (75, 0, 130),
                (148, 0, 211),
            ]
        )
        ukraine_colors = Colors(
            colors=[(0, 87, 183), (255, 215, 0)]
        )
        israel_colors = Colors(
            colors=[(0, 56, 184), (255, 255, 255)]
        )
        color_palette = choice([rainbow_colors, ukraine_colors, israel_colors])
        today = date.today()
        while time.time() < stop_time:
            if today not in chanukah_dates:
                menorah.fan_out(colors=color_palette.get_next(5), fade=.25)
            else:
                night = chanukah_dates.index(today) + 1
                menorah.color_chase(night, color=color_palette.get_next(), fade=1)
    except KeyboardInterrupt:
        menorah.off()
        print("\nPutting out the Menorah.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
