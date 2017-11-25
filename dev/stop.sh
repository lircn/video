#!/bin/sh

PROG="cap.py"

run=`ps ax|grep "$PROG"|grep -v "grep"`
if [ "$run" ]; then
    kill -9 `ps ax|grep "$PROG"|grep -v "grep"|awk '{print $1}'`
    kill -9 `ps ax|grep "ffmpeg"|grep -v "grep"|awk '{print $1}'`
    echo "$PROG stopped."
else
    echo "$PROG is not running."
fi
