# TODO: Make _lights_on and _lights_off not "private" or use light?
# TODO: Make these classes? or something more uniform
# Pattern class that sets everything it needs on init,
# then a run method that runs in every while loop?
# Doing this would allow things it do do things on init
# like randomly selecting or printing params)
# TODO: Some sort of alternating blinking (odds one color, evens another, then another color)
import time
import random


def to_bool(params, key):
    return params[key].lower()[0] == "t"


def fan_out(lamp, lights, palette, **kwargs):
    delay = float(kwargs["delay"])
    fade = float(kwargs["fade"])
    keep_on = to_bool(kwargs, "keep_on")
    # TODO: alternate (true = by light, false = by cycle)

    colors = palette.get_next(5)

    for i in range(5):
        color = colors[i % len(colors)]
        lights = [4 + i, 4 - i]
        lamp._lights_on(lights, [color], fade=fade)
        time.sleep(delay)
        if not keep_on:
            lamp._lights_off(lights, fade=fade)
    if keep_on:
        lamp.off(fade=fade)


def cycle(lamp, lights, palette, **kwargs):
    min_num = int(kwargs["min_num"])
    max_num = int(kwargs["max_num"])
    fade = float(kwargs["fade"])
    delay = float(kwargs["delay"])
    random_next = to_bool(kwargs, "random_next")
    reset = to_bool(kwargs, "reset")  # TODO: reset to off instead of next?

    if reset:
        lamp.light(lights, color=palette.get_next(), fade=fade)
        time.sleep(delay)

    num_lights = len(lights)
    if max_num <= 0:
        max_num = num_lights + max_num
    max_num = min(max_num, num_lights)

    if min_num <= 0:
        min_num = max_num
    min_num = min(min_num, max_num)

    # Now change them randomly
    num = random.randint(min_num, max_num)

    new_lights = lights[:]
    random.shuffle(new_lights)
    new_lights = new_lights[0:num]
    if random_next:
        new_colors = [random.choice(palette.get_all()) for _ in range(num)]
    else:
        new_colors = palette.get_next()

    lamp._lights_on(new_lights, new_colors, fade=fade)
    time.sleep(delay)


def color_chase(lamp, lights, palette, **kwargs):
    delay = float(kwargs["delay"])
    fade = float(kwargs["fade"])
    alternate = to_bool(kwargs, "alternate")

    num_lights = len(lights)
    palette_size_divides_lights = num_lights % palette.get_size() == 0

    color = palette.get_next()
    for idx, light in enumerate(lights):
        lamp._lights_on([light], [color], fade=fade)
        time.sleep(delay)
        if alternate and (
            (idx < num_lights - 1) or palette_size_divides_lights
        ):
            color = palette.get_next()


def snake(lamp, lights, palette, **kwargs):
    # TODO: Add flag to loop around (or bounce) instead of stopping at end then restarting
    # TODO: Always keep the shamash on?
    delay = float(kwargs["delay"])
    fade = float(kwargs["fade"])
    growing = to_bool(kwargs, "growing")
    snake_size = int(kwargs["snake_size"])
    white = to_bool(kwargs, "white")

    def snake_loop(palette, snake_size):
        if white:
            color = (255, 255, 255)
            off_color = palette.get_next()
        else:
            color = palette.get_next()
            off_color = (0, 0, 0)

        for snake_tail in range(num_lights):
            # Index of the head of the snake
            snake_head = snake_tail + snake_size - 1

            # Build the snake to start
            if snake_tail == 0:
                lamp._lights_on(lights[snake_tail], color, fade=fade)
                time.sleep(delay)
                for j in range(1, snake_size):
                    # print(f"{snake_tail}-P3")
                    lamp._lights_on(lights[j], color, fade=fade)
                    time.sleep(delay)

            # Remove the tail and move the head forward
            if snake_head < num_lights - 1:
                lamp._lights_on(
                    [lights[snake_tail], lights[snake_head + 1]],
                    [off_color, color],
                    fade=fade,
                )
                time.sleep(delay)
            elif snake_head == (num_lights - 1):
                # Remove remaining snake at end
                for j in range(snake_tail, snake_head + 1):
                    # print(f"{snake_tail}-P2-{j}")
                    lamp._lights_on(lights[j], off_color, fade=fade)
                    time.sleep(delay)  # Don't do this for the last one?
        if white:
            time.sleep(delay)

    num_lights = len(lights)
    if growing:
        for snake_size in range(1, num_lights + 1):
            snake_loop(palette, snake_size)
        time.sleep(delay)
    else:
        if snake_size < 0:
            snake_size = num_lights + snake_size
        # If snake_size is set to 0, this is the same as color_chase
        # so don't allow it
        snake_size = max(snake_size, 1)
        # If snake_size = num_lights, it's akin to color_chase
        # but has an "off" cycle so it is allowed
        snake_size = min(snake_size, num_lights)

        snake_loop(palette, snake_size)
