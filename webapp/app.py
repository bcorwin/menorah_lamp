from datetime import date
from subprocess import run
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/light", methods=["POST", "GET"])
def light():
  if request.method == "GET":
    return render_template("light.html", today=date.today())

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
    output = "Lighting the menorah."
  else:
    cmd = ["sudo", "../extinguish_menorah.sh"]
    output = "Putting out the menorah."
 
  run(cmd)
  return output

