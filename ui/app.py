import re
import sys
import inspect
from os import path
from datetime import date
import subprocess
from flask import Flask, render_template, request
from time import sleep, time

sys.path.append('/home/pi/menorah_lamp/lamp')
from patterns import all_patterns
from palettes import all_palettes
from pattern_templates import all_templates

app = Flask(__name__)
config_path = "/home/pi/menorah_lamp/config.yml"

def get_current_config():
    with open(config_path, "r") as file:
      yaml_string = file.read()
    if yaml_string:
      yaml_string = yaml_string.replace("\n", "<br>")
    return yaml_string

@app.route("/", methods=["GET"])
def config():
  output = render_template(
    "light.html",
    today=date.today(),
    palettes=all_palettes,
    patterns=all_patterns,
    templates=all_templates,
    config=get_current_config()
  )
  return output

@app.route("/set_state", methods=["POST"])
def set_state():
  d = request.form
  lighting = (d.get("light") == "")
  if lighting:
    cmd = ["sudo", "../light_menorah.sh"]
    cmd.extend(["--date", d["run_as_date"]])
    cmd.extend(["--run-time", str(int(d["run_length"]) / 60)])

    template = d["template"]
    if template != "None":
      cmd.extend(["--template", template])

    palette = d["palette"]
    if palette != "None":
      cmd.extend(["--colors", palette])

    pattern = d["pattern"]
    if pattern != "None":
      cmd.extend(["--pattern", pattern])

    params = d["params"]
    if params != "":
      for param in params.splitlines(keepends=False):
        param = re.search(r"(\w+)[\W]+([\w\.]+)", param)
        if param:
          key = param.group(1)
          value = param.group(2)
          cmd.extend(["--data", key, value])

    message = "Menorah configurations:"
  else:
    cmd = ["sudo", "../extinguish_menorah.sh"]
    message = "Menorah extinguished."

  process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=False
  )
  print("Running:", subprocess.list2cmdline(process.args))

  if lighting:
    sleep(1)
    for i in range(30):
      config_data = get_current_config()
      if config_data:
        break
      else:
        sleep(0.5)
  else:
    config_data = None

  output = render_template(
    "state.html",
    message=message,
    config=config_data,
  )
  return output

if __name__ == "__main__":
  app.run(host = "0.0.0.0", port = 5000)

