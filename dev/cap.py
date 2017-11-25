#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import subprocess
import urllib

g_url = "ai.nationz.com.cn"

cfg = {
    "input_dev" : "/dev/video0",
    "size_w" : 640,
    "size_h" : 480,

    "video_fmt" : "flv",
    "video_fps" : 12,
    "video_out" : "v.flv",
    #"video_out" : "rtmp://ai.nationz.com.cn:1935/myapp/testav",

    "image_fmt" : "image2",
    "image_fps" : 1,
    "image_out" : "/tmp/img/%03d.jpeg",

    "image_handler" : "./image_handler.sh",
}

config_file = "./config"

class Config:
    def load(self):
        try:
            with open(config_file, 'r') as f:
                for line in f:
                    if len(line) < 2 or line[0] == '#':
                        continue

                    kv = line.strip('\n')
                    kv = kv.split('=')
                    if cfg.has_key(kv[0]):
                        cfg[kv[0]] = kv[1]
        except IOError, e:
            print(str(e))

class Cap:
    def __init__(self):
        self.label_v = "[video]"
        self.label_i = "[image]"
        self.fd = None
        return

    def start(self):
        #print self.get_cmd()
        self.fd = subprocess.Popen(self.get_cmd(), stdout=None, stderr=None, shell=True)
        return

    def wait(self):
        self.fd.wait()
        return

    def stop(self):
        self.fd.terminate()
        return

    def get_cmd(self):
        cmd  = self.get_func()
        cmd += " -i %s " % (cfg["input_dev"])
        cmd += " -y -threads 1 -s " + self.get_size()
        cmd += " -lavfi '%s' " % (self.get_cfilter())

        cmd += " -map '%s' " % (self.label_v)
        cmd += " -f %s %s " % (cfg["video_fmt"], cfg["video_out"])

        cmd += " -map '%s' " % (self.label_i)
        cmd += " -f %s %s " % (cfg["image_fmt"], cfg["image_out"])
        return cmd

    def get_cfilter(self):
        v = "[_video]"
        i = "[_image]"
        ret = "split %s%s;%sfps=fps=%d%s;%sfps=fps=%d%s" % (v,i,v,int(cfg["video_fps"]),self.label_v,i,int(cfg["image_fps"]),self.label_i)
        return ret

    def get_func(self):
        return "ffmpeg"

    def get_size(self):
        ret = "%dx%d" % (int(cfg["size_w"]), int(cfg["size_h"]))
        return ret

class ImageProcess:
    def do(self):
        self.fd = subprocess.call(cfg["image_handler"], stdout=None, stderr=None, shell=True)
        return

def pull_info():
    usr = "bob"
    url = "http://" + g_url + "/usr_info/" + usr
    out = "/tmp/info/" + usr
    urllib.urlretrieve(url, out)
    return

if __name__ == '__main__':
    config = Config()
    config.load()

    cap = Cap()
    cap.start()

    imgp = ImageProcess()

    tik = 0
    # waiting for init
    time.sleep(3)

    while True:
        time.sleep(1)
        imgp.do()

        if tik % 60 == 0:
            pull_info()

        tik += 1
        if tik == 1000:
            tik = 0

    cap.stop()
    cap.wait()
    exit()
