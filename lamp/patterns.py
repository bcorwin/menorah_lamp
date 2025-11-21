# TODO: What is a template but a super or sub class of a pattern?
# They're the same except with different defaults
# and a potential subset of palettes to use (and checks if all params are set).
# How can I combine these concepts?
# Palette is used in Pattern to run,
# a list could be passed instead (or stored if a template)
import sys
import inspect
from random import choice

import pattern_functions as pf

class Pattern:
    def __init__(self, name, func, defaults={}):
        self.name = name
        self.func = func
        # TODO: Allow to be a list so I can make it so params don't conflict
        # TODO: Include template params (or use these instead??) as defaults
        self.defaults = defaults

        self.params = None
        self.lamp = None
        self.lights = None
        self.palette = None

    def _select_param(self, param):
        if isinstance(param, list) or isinstance(param, range):
            return choice(param)
        else:
            return param

    def get_name(self):
        return self.name

    def get_defaults(self, keys_only=False):
        if keys_only:
            return self.defaults.keys()
        else:
            return self.defaults

    def create(self, lamp, lights, palette, **kwargs):
        self.lamp = lamp
        self.lights = lights
        self.palette = palette

        params = {}
        for key, default in self.defaults.items():
            default_val = self._select_param(default)
            params[key] = str(kwargs.get(key, default_val))
        self.params = params

        return self.params

    def run(self):
        self.func(
            lamp=self.lamp,
            lights=self.lights,
            palette=self.palette,
            **self.params
        )


fan_out = Pattern(
    "Fan out",
    pf.fan_out,
    defaults = {
        "fade": 0.25,
        "delay": 0.25,
        "keep_on": [True, False]
    }
)

cycle = Pattern(
    "Cycle",
    pf.cycle,
    defaults = {
        "fade": 1.0,
        "delay": 1.0,
        "min_num": 1,
        "max_num": -1,
        "random_next": [False, True],
        "reset": True,
    }
)

color_chase = Pattern(
    "Color chase",
    pf.color_chase,
    defaults = {
        "fade": 1.0,
        "delay": 0.25,
        "alternate": [False, True],
    }
)

snake = Pattern(
    "Snake",
    pf.snake,
    defaults = {
        "delay": 0.25,
        "fade": 0.01,
        "growing": [False, True],
        "snake_size": range(1, 5),
    },
)

current_module = sys.modules[__name__]
all_patterns = {
    key: pattern
    for key, pattern in inspect.getmembers(current_module)
    if isinstance(pattern, Pattern)
}
