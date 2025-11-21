# TODO: Use this for some good looking (and named)
# default configs of Pattern / Palette / Params
# that could be used when selecting randomly
# instaed of always using random paletes and default params
import sys
import inspect
import random

from palettes import all_palettes
import patterns

all_palettes = list(all_palettes.values())
two_color_palettes = [p for p in all_palettes if p.get_size() == 2]

class DisplayTemplate:
    def __init__(self, name, pattern, palettes=all_palettes, params={}):
        self.name = name
        self.pattern = pattern
        self.palettes = palettes
        self.params = params
    def _select_param(self, param):
        if isinstance(param, list) or isinstance(param, range):
            return random.choice(param)
        else:
            return param
    def get_name(self):
        return self.name
    def get_pattern(self):
        return self.pattern
    def get_palette(self):
        return self._select_param(self.palettes)
    def get_params(self):
        out = {}
        for key, value in self.params.items():
            out[key] = str(self._select_param(value))
        return out


# Chaos: cycle, min_num = max_num = len(lights), reset = false, palette = rainbow? or other high count
# Sparkle: cycle, min_num = max_num = len(lights), reset = false, palette = low color count
# Alternate: something with even / odd 

blink = DisplayTemplate(
    name = "Blink",
    pattern = patterns.cycle,
    palettes = two_color_palettes,
    params = {
        "min_num": 0,
        "reset": False,
        "fade": 0,
        "delay": [x / 10 for x in range(2,6)]
    }
)

breath = DisplayTemplate(
    name = "Breath",
    pattern = patterns.cycle,
    params = {
        "min_num": 9,
        "max_num": 9,
        "reset": False,
        "fade": range(5, 11),
    }
)

sunrise = DisplayTemplate(
    name = "Sunrise",
    pattern = patterns.color_chase,
    params = {
        "fade": 10,
        "delay": 10,
        "alternate": True,
    }
)   

current_module = sys.modules[__name__]
all_templates = {
    key: template
    for key, template in inspect.getmembers(current_module)
    if isinstance(template, DisplayTemplate)
}
