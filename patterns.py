# TODO: Make this classes? or something more uniform
import time
import random


def fan_out(lamp, lights, palette, **kwargs):
    delay = kwargs.get("delay", 0.25)
    fade = kwargs.get("fade", 0.25)
    keep_on = kwargs.get("keep_on", True)

    colors = palette.get_next(5)

    if not isinstance(colors, list):
        colors = [colors]

    for i in range(5):
        color = colors[i % len(colors)]
        lights = [4+i, 4-i]
        lamp._lights_on(lights, [color], fade=fade)
        time.sleep(delay)
        if not keep_on:
            lamp._lights_off(lights, fade=fade)
    if keep_on:
        lamp.off(fade=fade)

def random(lamp, lights, palette, **kwargs):
    max_num = kwargs.get("max_num", len(lights))
    fade = kwargs.get("fade", 1)

    # Turn on all the lights to start
    lamp.light(lights, color=palette.get_next(), fade=fade)
    colors = palette.get_all()

    if max_num > len(lights):
        raise ValueError("max_num must be less than len(lights)")

    # Now change them randomly
    num = random.randint(1, max_num)
    new_lights = [random.choice(lights) for _ in range(num)]
    new_colors = [random.choice(colors) for _ in range(num)] 

    lamp._lights_on(new_lights, new_colors, fade=fade)

def color_chase(lamp, lights, palette, **kwargs):
    delay = kwargs.get("delay", 0.25)
    fade = kwargs.get("fade", 1)

    color = palette.get_next()

    for light in lights:
        lamp._lights_on([light], [color], fade=fade)
        time.sleep(delay)

def snake(lamp, lights, palette, **kwargs):
    # TODO: Could this replace color chase?
    # TODO: Add flag to loop around instead of stopping at end then restarting
    # TODO: Always keep the shamash on?
    # TODO: Implement growing:
    # elif pattern == "growing_snake":
    #     for snake_size in range(1, len(lights)):
    #         menorah.snake(lights, color=palette.get_next(), snake_size=snake_size)
    delay = kwargs.get("delay", 0.25)
    fade = kwargs.get("fade", 0.01)
    snake_size = kwargs.get("snake_size", 3)
    growing = kwargs.get("growing", False)

    color = palette.get_next()

    off_color = (0, 0, 0)
    num_lights = len(lights)
    if snake_size >= num_lights:
        raise ValueError("snake_size must be less than num_lights")

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
                fade = fade
            )
            time.sleep(delay)
        elif snake_head == (num_lights - 1):
            # Remove remaining snake at end
            for j in range(snake_tail, snake_head + 1):
                # print(f"{snake_tail}-P2-{j}")
                lamp._lights_off(lights[j], fade=fade)
                time.sleep(delay)  # Don't do this for the last one?
