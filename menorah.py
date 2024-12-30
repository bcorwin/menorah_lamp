#!/usr/bin/python3
# TODO: reformat
# TODO: spec out how to add and pick patterns

import os
import sys
import time
import colr
import click
import signal
import palettes as p
import holiday_dates as hd
from random import randint, choice, choices
from datetime import date, timedelta, datetime


signals = set(signal.Signals) - {signal.SIGKILL, signal.SIGSTOP} 

def handle_error(x,y):
    sys.exit(0)

for sig in signals:
    signal.signal(sig, handle_error)

class Menorah:
    def __init__(self, print_only=False):
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

        self.reverse = True
        self.shamash = 4
        
        try:
            interactive = os.getpgrp() == os.tcgetpgrp(sys.stdout.fileno())
        except Exception:
            interactive = False
        self.interactive = interactive

        self.print_only = print_only
        
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

    # Fun patterns
    def fan_out(self, colors=(255, 255, 255), delay=0.25, fade=0, keep_on=True):
        if not isinstance(colors, list):
            colors = [colors]

        for i in range(5):
            color = colors[i % len(colors)]
            lights = [4+i, 4-i]
            self._lights_on(lights, [color], fade=fade)
            time.sleep(delay)
            if not keep_on:
                self._lights_off(lights, fade=fade)
        if keep_on:
            self.off(fade=fade)

    def color_chase(self, lights, color=(255, 255, 255), delay=0.25, fade=0):
        for light in lights:
            self._lights_on([light], [color], fade=fade)
            time.sleep(delay)

    def snake(self, lights, color=(255, 255, 255), delay=0.25, fade=0.01, snake_size=3):
        # TODO: Could this replace color chase?
        # TOOD: Add flag to loop around instead of stopping at end then restarting
        off_color = (0, 0, 0)
        num_lights = len(lights)
        if snake_size >= num_lights:
            raise ValueError("snake_size must be less than num_lights")

        for snake_tail in range(num_lights):
            # Index of the head of the snake
            snake_head = snake_tail + snake_size - 1

            # Build the snake to start
            if snake_tail == 0:
              self._lights_on(lights[snake_tail], color, fade=fade)
              time.sleep(delay)
              for j in range(1, snake_size):
                # print(f"{snake_tail}-P3")
                self._lights_on(lights[j], color, fade=fade)
                time.sleep(delay)

            # Remove the tail and move the head forward
            if snake_head < num_lights - 1:             
              self._lights_on(
                  [lights[snake_tail], lights[snake_head + 1]],
                  [off_color, color],
                  fade = fade
              )
              time.sleep(delay)
            elif snake_head == (num_lights - 1):
              # Remove remaining snake at end
              for j in range(snake_tail, snake_head + 1):
                  # print(f"{snake_tail}-P2-{j}")
                  self._lights_off(lights[j], fade=fade)
                  time.sleep(delay)  # Don't do this for the last one?
    
    def random(self, lights, colors, max_num=None, fade=0):
        if max_num is None:
            max_num = len(lights)
        assert max_num <= len(lights), "max_num must be less than len(lights)"
        
        num = randint(1, max_num)
        new_lights = [choice(lights) for _ in range(num)]
        new_colors = [choice(colors) for _ in range(num)] 
                
        self._lights_on(new_lights, new_colors, fade=fade)

    def blink(self, lights, delay=0.1, fade=0):
        colors = self._get_colors(lights)
        self._lights_off(lights, fade=fade)
        time.sleep(delay)
        self._lights_on(lights, colors, fade=fade)

    def print(self, message, log=True, **kwargs):
      if log:
        with open(self.config_file, "a") as f:
          f.write(str(message) + "\n")
        
      if self.interactive:
        print(message, **kwargs)

@click.command()
@click.option("--date",
    "date_to_run",
    default=str(date.today()),
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Date to run as.")
@click.option("--sleep",
    default=4.5,
    type=click.FLOAT,
    help="How long to run for (in hours).")
@click.option("--palette", "-p",
    default=None,
    help="Palette name. See palettes.py for options.")
@click.option("--keep-on/--no-keep-on",
    default=None,
    help="Keep on for the fan_out pattern.")
@click.option("--pattern",
    default=None,
    help="Pattern to use."
)
def main(date_to_run=None, sleep=None, palette=None, keep_on=None, pattern=None):
    stop_time = time.time() + 60 * 60 * sleep
    try:
        menorah = Menorah()
        patterns = ["fan_out", "color_chase", "random", "snake", "growing_snake"]

        date_to_run = date_to_run.date()
        menorah.print(f"Date: {date_to_run}")
        night = hd.chanukah_nights.get(date_to_run)
        if night is not None:
            lights = menorah.get_lights(night)
            patterns.remove("fan_out")
            menorah.print(f"Night: {night}")
        else:
            lights = menorah.get_lights(8)
            menorah.print("Night: Not yet Chanukah, using all lights", log=False)

        if palette is not None:
            if not hasattr(p, palette):
                raise ValueError("Invalid palette")
            else:
                palette = getattr(p, palette)
                assert isinstance(palette, p.Colors), "Palette is not a palette"
        else:
            if date_to_run in hd.christmas_dates:
                palette = p.christmas
            elif date_to_run in hd.shabbat_dates:
                palette = p.israel
            else:
               palette = p.random()
        menorah.print(f"Palette: {palette}")

        if keep_on is None:
            keep_on = choice([True, False])

        if pattern is None:
            pattern = choice(patterns)
        else:
            assert pattern in patterns, f"Invalid pattern name: {pattern}"
        menorah.print(f"Pattern: {pattern}")

        while time.time() < stop_time:
            if pattern == "fan_out":
                menorah.fan_out(colors=palette.get_next(5), fade=.25, keep_on=keep_on)
            elif pattern == "color_chase":
                menorah.color_chase(lights, color=palette.get_next(), fade=1)
            elif pattern == "blink":
                # TODO: Make this better before using it. It's boring.
                menorah.light(lights, color=palette.get_next(), fade=1)
                for _ in range(10):
                    blink_lights = choices(lights,
                                           k=randint(0, len(lights) // 3))
                    menorah.blink(blink_lights, fade=0.1)
                    time.sleep(0.1)
            elif pattern == "random":
                menorah.light(lights, color=palette.get_next(), fade=1)
                menorah.random(lights, colors=palette.get_all(), fade=1)
            elif pattern == "snake":
                num_lights = len(lights)
                snake_size = 3 if num_lights > 3 else num_lights - 1
                menorah.snake(lights, color=palette.get_next(), snake_size = snake_size)
            elif pattern == "growing_snake":
                for snake_size in range(1, len(lights)):
                    menorah.snake(lights, color=palette.get_next(), snake_size=snake_size)
            # TODO: Add Magni-phi effect (or is this just color chase?)

    finally:
        menorah.off()
        menorah.print("\n\nPutting out the Menorah.\033[?25h", log=False)


if __name__ == '__main__':
    main()
