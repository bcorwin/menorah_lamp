from random import choice


class Colors:

    def __init__(self, name, colors):
        self.current = 0
        self.name = name
        self.colors = colors

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


WHITE = (255, 255, 255)

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

def random():
    return choice([rainbow, ukraine, israel, v_day, patriotic])

