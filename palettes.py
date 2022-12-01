from random import choice


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

rainbow = Colors(
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
ukraine = Colors(colors=[(0, 87, 183), (255, 215, 0)])
israel = Colors(colors=[(0, 56, 184), (255, 255, 255)])
christmas = Colors(colors=[(0, 179, 44), (179, 0, 12)])

def random():
    return choice([rainbow, ukraine, israel])
