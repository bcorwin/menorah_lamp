import sys
import inspect

import pattern_functions as pf

class Pattern:
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def get_name(self):
        return self.name

    def create(self, lamp, lights, palette, **kwargs):
        self.lamp = lamp
        self.lights = lights
        self.palette = palette
        self.params = kwargs

    def run(self):
        self.func(
            lamp=self.lamp,
            lights=self.lights,
            palette=self.palette,
            **self.params
        )


fan_out = Pattern("Fan out", pf.fan_out)

cycle = Pattern("Cycle", pf.cycle)

color_chase = Pattern("Color chase", pf.color_chase)

snake = Pattern("Snake", pf.snake)

current_module = sys.modules[__name__]
all_patterns = {
    key: pattern
    for key, pattern in inspect.getmembers(current_module)
    if isinstance(pattern, Pattern)
}
