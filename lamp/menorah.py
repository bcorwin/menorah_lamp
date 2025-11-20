import sys
import time
import colr
import inspect

import patterns

all_patterns = {
    key: pattern
    for key, pattern in inspect.getmembers(patterns)
    if isinstance(pattern, patterns.Pattern)
}

class Menorah:
    def __init__(self, print_only=False):
        self.reverse = True
        self.shamash = 4
        self.interactive = sys.stdin.isatty()
        self.print_only = print_only
        self.config_file = "config.txt"

        with open(self.config_file, "w") as f:
          f.write("")

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
        
        self.print("Lighting the Menorah. Ctrl-C to put it out.", log=False)

    def __str__(self):
        colors = self._get_colors()
        colors = ['#%02x%02x%02x' % c for c in colors]

        row1 = [" " if i != self.shamash else colr.color("╻", fore=colors[i]) for i in range(8, -1, -1)] 
        row2 = [colr.color("╻", fore=colors[i]) if i != self.shamash else "│" for i in range(8, -1, -1)]

        row1 = " ".join(row1)
        row2 = " ".join(row2)
        out = row1 + "\n" + row2
        out += "\n╰─┴─┴─┴─┼─┴─┴─┴─╯"
        out += "\n    ════╧════    "
        return out

    def _get_colors(self, lights=None):
        if lights is None:
            lights = list(range(9))
        out = [self.pixels[i] for i in lights]
        if self.pixel_order == "GRB":
            out = [(x[1], x[0], x[2]) for x in out]
        return out
 
    def _led_on(self, led, color):
        if not self.print_only:
            if self.pixel_order == "GRB":
                color = (color[1], color[0], color[2])
            self.pixels[led] = color
            self.pixels.show()

    def _led_off(self, led):
        self._led_on(led, (0, 0, 0))

    def _fade(self, lights, colors, fade_time, num_steps=100):
        start = self._get_colors(lights)
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
        if not isinstance(lights, list):
            lights = [lights]
        if not isinstance(colors, list):
            colors = [colors]

        if len(colors) == 1:
            colors = len(lights)*colors
        assert len(colors) == len(lights), \
            "Length of colors and lights must match (or set colors as single string)"

        if fade <= 0:
            for i in range(len(lights)):
                self._led_on(lights[i], colors[i])
        else:
            self._fade(lights, colors, fade_time=fade)

        self.print(self, end="\033[A\033[A\033[A\r\033[?25l", log=False)

    def _lights_off(self, lights, fade=0):
        if not isinstance(lights, list):
            lights = [lights]
        self._lights_on(lights, len(lights)*[(0,0,0)], fade=fade)

    def get_lights(self, night):
        assert night >= 1, "Night must be at least 1"
        assert night <= 8, "Night can't be more than 8"

        lights = list(range(9))
        if self.reverse:
            lights.reverse()
        lights.pop(self.shamash)
        lights = lights[-night:]
        lights = [self.shamash] + lights
        return lights

    def off(self, fade=0):
        self._lights_off(list(range(9)), fade=fade)

    def light(self, lights, color=(255, 255, 255), fade=0):
        self._lights_on(lights, [color], fade=fade)

    def print(self, message, log=True, **kwargs):
      if log:
        with open(self.config_file, "a") as f:
          f.write(str(message) + "\n")
        
      if self.interactive:
        print(message, **kwargs)