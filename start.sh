#!/bin/sh

PROG="cap.py"

mkdir -p /tmp/img/

run=`ps ax|grep "$PROG"|grep -v "grep"`
if [ "$run" ]; then
    echo "$PROG is already running"
    exit
fi

(./$PROG > /dev/null &)
echo "$PROG start."
