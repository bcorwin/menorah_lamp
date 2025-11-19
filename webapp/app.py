import sys
import inspect
from os import path
from datetime import date
import subprocess
from flask import Flask, render_template, request
from time import sleep, time


sys.path.append('../')
import palettes
import patterns

app = Flask(__name__)

palette_names = {
    name: str(obj)
    for name, obj in inspect.getmembers(palettes)
    if isinstance(obj, palettes.Colors)
}

pattern_names = {
    name: name
    for name, obj in inspect.getmembers(patterns)
    if callable(obj)
}

@app.route("/", methods=["GET"])
def config():
  output = render_template(
    "light.html",
    today=date.today(),
    palettes=palette_names,
    patterns=pattern_names,
  )
  return output

@app.route("/set_state", methods=["POST"])
def set_state():
  d = request.form
  lighting = (d.get("light") == "")
  if lighting:
    cmd = ["sudo", "../light_menorah.sh"]
    cmd.extend(["--date", d["run_as_date"]])
    cmd.extend(["--sleep", d["run_length"]])

    palette = d["palette"]
    if palette != "None":
      cmd.extend(["--colors", palette])

    pattern = d["pattern"]
    if pattern != "None":
      cmd.extend(["--pattern", pattern])

    message = "Menorah lit:"
  else:
    cmd = ["sudo", "../extinguish_menorah.sh"]
    message = "Menorah extinguished."

  process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=False
  )

  if lighting:
    config_path = "config.txt"
    while (time() - path.getmtime(config_path)) > 1:
      sleep(0.5)
    with open(config_path) as f:
      cmd_output = f.read().strip()
    cmd_output = cmd_output.split("\n")
  else:
    cmd_output = None

  output = render_template(
    "state.html",
    message=message,
    cmd_output=cmd_output,
  )
  return output

if __name__ == "__main__":
  app.run(host = "0.0.0.0", port = 5000)

