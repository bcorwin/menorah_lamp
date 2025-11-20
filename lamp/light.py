#!/usr/bin/python3
# TODO: reformat
import sys
import time
import click
import signal
from random import choice
from datetime import date

from menorah import Menorah, pattern_names
import palettes

import holiday_dates as hd

# TODO: Make this a dictionary (name, obj) and move to Menorah
import inspect
palette_names = [
    name
    for name, obj in inspect.getmembers(palettes)
    if isinstance(obj, palettes.Colors)
]

signals = set(signal.Signals) - {signal.SIGKILL, signal.SIGSTOP} 

def handle_error(x,y):
    sys.exit(0)

for sig in signals:
    signal.signal(sig, handle_error)


@click.command()
@click.option(
    "--date",
    "date_to_run",
    default=str(date.today()),
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Date to run as."
)
@click.option(
    "--sleep",
    default=4.5,
    type=click.FLOAT,
    help="How long to run for (in hours)."
)
@click.option(
    "--colors",
    "-c",
    "palette",
    default=None,
    type=click.Choice(palette_names, case_sensitive=False),
    help="Palette name / color-set to use."
)
@click.option(
    "--pattern",
    "-p",
    default=None,
    type=click.Choice(pattern_names, case_sensitive=False),
    help="Pattern to use."
)
@click.option(
    "--data",
    "-d",
    help="Additional data (parameters) to pass to the chosen pattern.",
    type=(str, str),
    multiple=True
)
def light(date_to_run=None, sleep=None, palette=None, pattern=None, data=None):
    stop_time = time.time() + 60 * 60 * sleep
    try:
        menorah = Menorah()

        date_to_run = date_to_run.date()
        menorah.print(f"Date: {date_to_run}")

        night = hd.chanukah_nights.get(date_to_run)
        if night is not None:
            lights = menorah.get_lights(night)
            pattern_names.remove("fan_out")
            menorah.print(f"Night: {night}")
        else:
            lights = menorah.get_lights(8)
            menorah.print("Night: Not yet Chanukah, using all lights", log=False)

        if palette is not None:
            palette = getattr(palettes, palette.lower())
        else:
            if date_to_run in hd.christmas_dates:
                palette = palettes.christmas
            elif date_to_run in hd.shabbat_dates:
                palette = palettes.israel
            else:
               palette = getattr(palettes, choice(palette_names))
        menorah.print(f"Palette: {palette}")

        if pattern is None:
            pattern = choice(pattern_names)
        menorah.print(f"Pattern: {pattern}")

        params = dict(data)
        menorah.print(f"Params: {params}")

        while time.time() < stop_time:
            menorah.run_pattern(
                pattern=pattern.lower(),
                lights=lights,
                palette=palette,
                **params
            )

    finally:
        menorah.off()
        menorah.print("\n\nPutting out the Menorah.\033[?25h", log=False)


if __name__ == '__main__':
    light()
