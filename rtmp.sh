#!/bin/sh
# Author: zaynli <zaynli@tencent.com>

ffmpeg -f video4linux2 -r 12 -s 640x480 -i /dev/video0 -f flv rtmp://ai.nationz.com.cn:1935/myapp/testav
