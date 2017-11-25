#!/bin/sh

PROG="cap.py"

mkdir -p /tmp/img/
mkdir -p /tmp/info/

run=`ps ax|grep "$PROG"|grep -v "grep"`
echo $run
if [ "$run" ]; then
    echo "$PROG is already running"
    exit
fi

(python $PROG > /dev/null &)
echo "$PROG start."
