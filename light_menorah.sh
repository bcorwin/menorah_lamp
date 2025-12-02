#!/bin/bash

# DO NOT USE THIS IF YOU WANT TO RUN IT INTERACTIVELY.
# TO RUN INTERACTIVELY RUN ./lamp/light.py

pid_file=/home/pi/menorah_lamp/app.pid
log_file=/home/pi/menorah_lamp/log.txt

if [ "$EUID" -ne 0 ]; then
  echo "This script must be run with sudo or as the root user."
  exit 1
fi

exec >> $log_file 2>&1

if [ -f "$pid_file" ]; then
    bash /home/pi/menorah_lamp/extinguish_menorah.sh
fi

echo "`date` Lighting the menorah"
python3 /home/pi/menorah_lamp/lamp/light.py $@ &
pid=$!
echo $pid > $pid_file
# disown $pid

echo "`date` Done lighting the menorah"
exit 0
