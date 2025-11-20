# DO NOT USE THIS IF YOU WANT TO RUN IT INTERACTIVELY.
# TO RUN INTERACTIVELY RUN ./menorah.py

# TODO: run menorah in background so this can exit and I don't need ctrl-c
# TODO: Fix the way things print to the terminal
# TODO: Print errors to log?
# TODO: use extinguish_menorah.sh instead

pid_file=/home/pi/menorah_lamp/app.pid
log_file=/home/pi/menorah_lamp/log.txt

if [ -f "$pid_file" ]; then
    echo "`date` Turning off pervious lighting"
    sudo kill -s SIGINT `cat $pid_file` || true
    sudo rm $pid_file
fi

echo "`date` Lighting the menorah"
python3 /home/pi/menorah_lamp/lamp/light.py $@ &
pid=$!
echo $pid > $pid_file
# disown $pid

echo "`date` Done lighting the menorah"
exit 0
