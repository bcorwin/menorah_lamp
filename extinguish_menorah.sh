#!/bin/bash

pid_file=/home/pi/menorah_lamp/app.pid

if [ -f "$pid_file" ]; then
    echo "`date` Extinguishing the menorah"
    sudo kill -s SIGINT `cat $pid_file` || true
    sudo rm $pid_file
fi
