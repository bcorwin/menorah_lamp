#!/usr/bin/python3
# TODO: reformat
import sys
import time
import click
import signal
from random import choice
from datetime import date

import holiday_dates as hd
from pattern_templates import PatternTemplate, all_templates
from menorah import Menorah
from palettes import all_palettes
from patterns import all_patterns

signals = set(signal.Signals) - {signal.SIGKILL, signal.SIGSTOP} 

def handle_error(x,y):
    sys.exit(0)

for sig in signals:
    signal.signal(sig, handle_error)

@click.command()
@click.option(
    "--color-set",
    "-c",
    "palette_key",
    default=None,
    type=click.Choice(sorted(all_palettes.keys()), case_sensitive=False),
    metavar='PALETTE',
    help="Palette (color-set) name."
)
@click.option(
    "--pattern",
    "-p",
    "pattern_key",
    default=None,
    type=click.Choice(sorted(all_patterns.keys()), case_sensitive=False),
    metavar='PATTERN',
    help="Pattern name."
)
@click.option(
    "--template",
    "-t",
    "template_key",
    default=None,
    type=click.Choice(sorted(all_templates.keys()), case_sensitive=False),
    metavar='TEMPLATE',
    help="Template name, overrides pattern and data selections."
)
@click.option(
    "--data",
    "-d",
    help="Parameters (data) to pass to the pattern.",
    type=(str, str),
    multiple=True
)
@click.option(
    "--date",
    "date_to_run",
    default=str(date.today()),
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Date to run as."
)
@click.option(
    "--run-time",
    default=4.5,
    type=click.FLOAT,
    help="How long to run for (in hours)."
)
def light(palette_key, pattern_key, template_key, data, date_to_run, run_time):
    stop_time = time.time() + 60 * 60 * run_time
    try:
        menorah = Menorah()

        date_to_run = date_to_run.date()
        menorah.print({"Date": str(date_to_run)})

        night = hd.chanukah_nights.get(date_to_run)
        if night is not None:
            lights = menorah.get_lights(night)
            _ = all_patterns.pop("fan_out")
            menorah.print({"Night": night})
        else:
            lights = menorah.get_lights(8)
            menorah.print({"Night": "N/A (using all lights)"})

        if template_key:
            pattern = all_templates[template_key.lower()]
        elif pattern_key is None:
            pattern_key, pattern = choice(
                list(all_patterns.items()) +
                list(all_templates.items())
            )
        else:
            pattern = all_patterns[pattern_key.lower()]
        menorah.print({"Pattern": pattern.get_name()})

        if palette_key is not None:
            palette = all_palettes[palette_key.lower()]
        else:
            if date_to_run in hd.christmas_dates:
                palette = all_palettes['christmas']
            elif date_to_run in hd.shabbat_dates:
                palette = all_palettes['israel']
            elif isinstance(pattern, PatternTemplate):
                palette = pattern.get_palette()
            else:
                palette_key = choice(list(all_palettes.keys()))
                palette = all_palettes[palette_key]
        menorah.print({"Palette": palette.get_name()})

        params = dict(data)
        all_params = pattern.create(menorah, lights, palette, **params)
        menorah.print({"Params": all_params})

        while time.time() < stop_time:
            pattern.run()

    finally:
        menorah.off()
        menorah.print("\n\nPutting out the Menorah.\033[?25h", log=False)

if __name__ == '__main__':
    light()
