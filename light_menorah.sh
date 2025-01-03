# DO NOT USE THIS IF YOU WANT TO RUN IT INTERACTIVELY.
# TO RUN INTERACTIVELY RUN ./menorah.py

# TODO: run menorah in background so this can exit and I don't need ctrl-c
# TODO: Fix the way things print to the terminal
# TODO: Print errors to log?
# TODO: use extinguish_menorah.sh instead

pid_file=/home/pi/menorah_lamp/app.pid

if [ -f "$pid_file" ]; then
    sudo kill -s SIGINT `cat $pid_file` || true
    sudo rm $pid_file
fi

python3 /home/pi/menorah_lamp/menorah.py $@ &
pid=$!
echo $pid > $pid_file
# disown $pid
