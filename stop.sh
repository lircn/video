#!/bin/sh

PROG="cap.py"

if [ ! -x "$PROG" ]; then
    echo "$PROG is not exist. exit now."
    exit
fi

run=`ps ax|grep "$PROG"|grep -v "grep"`
if [ "$run" ]; then
    kill -9 `ps ax|grep "$PROG"|grep -v "grep"|cut -d " " -f 1`
    kill -9 `ps ax|grep "ffmpeg"|grep -v "grep"|cut -d " " -f 1`
    echo "$PROG stopped."
else
    echo "$PROG is not running."
fi
