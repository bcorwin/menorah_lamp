import sys
import inspect
from random import choice

WHITE = (255, 255, 255)


class Colors:

    def __init__(self, name, colors):
        self.current = 0
        self.name = name
        self.colors = colors

    def get_size(self):
        return len(self.colors)

    def get_name(self):
        return self.name

    def get_all(self):
        return self.colors

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
    
    def __str__(self):
        return self.name

rainbow = Colors(
    name="Rainbow",
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

ukraine = Colors(name="Ukraine", colors=[(0, 87, 183), (255, 215, 0)])

israel = Colors(name="Israel", colors=[(0, 56, 184), WHITE])

christmas = Colors(name="Christmas", colors=[(0, 150, 2), (229, 0, 0)])

v_day = Colors(
    name="V-day",
    colors=[
        (255,197,230), 
        (255, 37, 126),
        (255,38,68),
        (214,0,0)
    ]
)

patriotic = Colors(
    name = "Patriotic",
    colors=[
        (255, 255, 255),
        (200,  16,  46),
        (  1,  33, 105),
    ]
)

rgb = Colors(
    name = "RGB",
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
    ]
)

starry_night = Colors(
    name = "Starry Night Serenade",
    colors = [
        (13, 69, 100),
        (100, 84, 0),
        (100, 13, 55),
    ]
)

purples = Colors(
    name = "Purples",
    colors = [
        (84, 8, 99),
        (146, 72, 122),
        (228, 155, 166),
        (255, 211, 213),
    ]
)

mexico = Colors(
    name="Mexico",
    colors=[
        (0, 200, 65),
        WHITE,
        (200, 16, 46),
    ]
)

canada = Colors(
    name="Canada",
    colors=[
        (216, 6, 33),
        WHITE,
    ]
)

# TODO: Improve the colors
vermont = Colors(
    name = "Vermont",
    colors = [
        (0, 51, 102),
        (90, 133, 98),
        (255, 204, 51),
    ]
)

current_module = sys.modules[__name__]
all_palettes = {
    key: palette
    for key, palette in inspect.getmembers(current_module)
    if isinstance(palette, Colors)
}
