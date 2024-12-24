from datetime import date
import subprocess
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET"])
def config():
  output = render_template(
    "light.html",
    today=date.today()
 )
  return output

@app.route("/set_state", methods=["POST"])
def set_state():
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
  #results = run(cmd)
  output = subprocess.check_output(cmd, text=True, timeout=10)

  print(output)
  return redirect(url_for("view"))

@app.route("/view", methods=["GET"])
def view():
  return "Viewing"
