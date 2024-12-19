from datetime import date
from subprocess import run
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def light():
  if request.method == "POST":
    d = request.form
    if d.get("light") == "":
      cmd = ["sudo", "../light_menorah.sh"]
      cmd.extend(["--date", d["run_as_date"]])
      cmd.extend(["--sleep", d["run_length"]])

      palette = d["palette"]
      if palette != "None":
        cmd.extend(["--palette", palette])

      pattern = d["pattern"]
      if pattern != "None":
        cmd.extend(["--pattern", pattern])  
      message = "Lighting the menorah."
    else:
      cmd = ["sudo", "../extinguish_menorah.sh"]
      message = "Putting out the menorah."
    run(cmd)
  else:
    message = None
  
  output = render_template(
    "light.html",
    today=date.today(),
    message = message
  )
  return output

