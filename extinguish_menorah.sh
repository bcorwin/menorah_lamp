pid_file=/home/pi/menorah_lamp/app.pid

if [ -f "$pid_file" ]; then
    sudo kill -s SIGINT `cat $pid_file` || true
    rm $pid_file
fi
