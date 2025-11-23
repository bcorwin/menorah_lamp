import sys
import inspect
import random

from palettes import all_palettes, WHITE
import patterns

all_palettes = list(all_palettes.values())
two_color_palettes = [p for p in all_palettes if p.get_size() == 2]
non_white_palettes = [p for p in all_palettes if WHITE not in p.get_all()]

class PatternTemplate(patterns.Pattern):
    def __init__(self, name, pattern, palettes=all_palettes, params={}):
        if params.keys() != pattern.get_defaults(keys_only=True):
            raise RuntimeError("All params must be set in a pattern.")

        pattern_name = pattern.get_name()
        name = f"{name} ({pattern_name})"

        super().__init__(name, pattern.func, defaults=params)
        self.palettes = palettes

    def get_palette(self):
        return self._select_param(self.palettes)

    def create(self, lamp, lights, palette, **kwargs):
        # Drop kwargs so it uses the params set in the template
        return super().create(lamp, lights, palette)


# Chaos: cycle, min_num = max_num = len(lights), reset = false, palette = rainbow? or other high count
# Sparkle: cycle, min_num = max_num = len(lights), reset = false, palette = low color count
# Alternate: something with even / odd 

blink = PatternTemplate(
    name = "Blink",
    pattern = patterns.cycle,
    palettes = two_color_palettes,
    params = {
        "fade": 0,
        "delay": [x / 10 for x in range(2,6)],
        "min_num": 0,
        "max_num": 0,
        "random_next": False,
        "reset": False,
    }
)

breath = PatternTemplate(
    name = "Breath",
    pattern = patterns.cycle,
    params = {
        "fade": range(5, 11),
        "delay": 1.0,
        "min_num": 0,
        "max_num": 0,
        "reset": False,
        "random_next": False,
        "reset": False,
    }
)

sunrise = PatternTemplate(
    name = "Sunrise",
    pattern = patterns.color_chase,
    params = {
        "fade": 10,
        "delay": 10,
        "alternate": True,
    }
)

white_snake = PatternTemplate(
    name = "White snake",
    pattern = patterns.snake,
    palettes = non_white_palettes,
    params = {
        "delay": 0.25,
        "fade": 0.01,
        "growing": False,
        "snake_size": 1,
        "white": True,
    }
)

current_module = sys.modules[__name__]
all_templates = {
    key: template
    for key, template in inspect.getmembers(current_module)
    if isinstance(template, PatternTemplate)
}
