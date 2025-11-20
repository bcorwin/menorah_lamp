# TODO: Make these classes? or something more uniform
# Pattern class that sets everything it needs on init,
# then a run method that runs in every while loop?
# Doing this would allow things it do do things on init
# like randomly selecting or printing params)
# TODO: Some sort of alternating blinking (odds one color, evens another, then another color)
import time
import random

def fan_out(lamp, lights, palette, **kwargs):
    delay = float(kwargs.get("delay", 0.25))
    fade = float(kwargs.get("fade", 0.25))
    keep_on = kwargs.get("keep_on", "true").lower()[0] == "t"

    colors = palette.get_next(5)

    for i in range(5):
        color = colors[i % len(colors)]
        lights = [4+i, 4-i]
        lamp._lights_on(lights, [color], fade=fade)
        time.sleep(delay)
        if not keep_on:
            lamp._lights_off(lights, fade=fade)
    if keep_on:
        lamp.off(fade=fade)

def cycle(lamp, lights, palette, **kwargs):
    max_num = int(kwargs.get("max_num", len(lights)))
    fade = float(kwargs.get("fade", 1))
    delay = float(kwargs.get("delay", 1))
    random_next = kwargs.get("random_next", "false").lower()[0] == "t"
    reset = kwargs.get("reset", "true").lower()[0] == "t"

    if reset:
        lamp.light(lights, color=palette.get_next(), fade=fade)
        time.sleep(delay)

    if max_num > len(lights):
        raise ValueError("max_num must be less than len(lights)")

    # Now change them randomly
    num = random.randint(1, max_num)
    new_lights = [random.choice(lights) for _ in range(num)]
    if random_next:
        new_colors = [random.choice(palette.get_all()) for _ in range(num)]
    else:
        new_colors = palette.get_next()

    lamp._lights_on(new_lights, new_colors, fade=fade)
    time.sleep(delay)

def color_chase(lamp, lights, palette, **kwargs):
    delay = float(kwargs.get("delay", 0.25))
    fade = float(kwargs.get("fade", 1))

    color = palette.get_next()

    for light in lights:
        lamp._lights_on([light], [color], fade=fade)
        time.sleep(delay)

def snake(lamp, lights, palette, **kwargs):
    # TODO: Could this replace color chase?
    # TODO: Add flag to loop around instead of stopping at end then restarting
    # TODO: Always keep the shamash on?
    delay = float(kwargs.get("delay", 0.25))
    fade = float(kwargs.get("fade", 0.01))
    growing = kwargs.get("growing", 'false').lower()[0] == 't'
    snake_size = int(kwargs.get("snake_size", 0))

    def snake_loop(color, snake_size):
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
                    fade = fade
                )
                time.sleep(delay)
            elif snake_head == (num_lights - 1):
                # Remove remaining snake at end
                for j in range(snake_tail, snake_head + 1):
                    # print(f"{snake_tail}-P2-{j}")
                    lamp._lights_off(lights[j], fade=fade)
                    time.sleep(delay)  # Don't do this for the last one?

    num_lights = len(lights)
    if growing:
        for snake_size in range(1, num_lights):
            snake_loop(palette.get_next(), snake_size)
        time.sleep(delay)
    else:
        if not snake_size:
            snake_size = 3 if num_lights > 3 else num_lights - 1
        if snake_size >= num_lights:
            raise ValueError("snake_size must be less than num_lights")

        snake_loop(palette.get_next(), snake_size)
