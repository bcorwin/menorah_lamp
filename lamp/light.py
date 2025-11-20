#!/usr/bin/python3
# TODO: reformat
import sys
import time
import click
import signal
from random import choice
from datetime import date

from menorah import Menorah, all_patterns, all_palettes
import holiday_dates as hd

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
    "palette_key",
    default=None,
    type=click.Choice(sorted(all_palettes.keys()), case_sensitive=False),
    help="Palette name / color-set to use."
)
@click.option(
    "--pattern",
    "-p",
    "pattern_key",
    default=None,
    type=click.Choice(sorted(all_patterns.keys()), case_sensitive=False),
    help="Pattern to use."
)
@click.option(
    "--data",
    "-d",
    help="Additional data (parameters) to pass to the chosen pattern.",
    type=(str, str),
    multiple=True
)
def light(date_to_run=None, sleep=None, palette_key=None, pattern_key=None, data=None):
    stop_time = time.time() + 60 * 60 * sleep
    try:
        menorah = Menorah()

        date_to_run = date_to_run.date()
        menorah.print(f"Date: {date_to_run}")

        night = hd.chanukah_nights.get(date_to_run)
        if night is not None:
            lights = menorah.get_lights(night)
            _ = all_patterns.pop("fan_out")
            menorah.print(f"Night: {night}")
        else:
            lights = menorah.get_lights(8)
            menorah.print("Night: Not yet Chanukah, using all lights", log=False)

        if palette_key is not None:
            palette = all_palettes[palette_key.lower()]
        else:
            if date_to_run in hd.christmas_dates:
                palette_key = 'christmas'
            elif date_to_run in hd.shabbat_dates:
                palette_key = 'israel'
            else:
               palette_key = choice(list(all_palettes.keys()))
            palette = all_palettes[palette_key]
        menorah.print(f"Palette: {palette.get_name()}")

        if pattern_key is None:
            pattern_key, pattern = choice(list(all_patterns.items()))
        else:
            pattern = all_patterns[pattern_key.lower()]
        menorah.print(f"Pattern: {pattern.get_name()}")

        params = dict(data)
        menorah.print(f"Params: {params}")

        pattern.create(menorah, lights, palette, **params)
        while time.time() < stop_time:
            pattern.run()

    finally:
        menorah.off()
        menorah.print("\n\nPutting out the Menorah.\033[?25h", log=False)


if __name__ == '__main__':
    light()
