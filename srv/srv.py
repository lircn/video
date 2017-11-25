#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import os
import time
import json

OK = 0
ERR = -1

srv_port = 10419

class LoginModule:
    def __init__(self):
        self.data = {
            "alice": "123",
            "bob": "123",
        }
        return

    def check_usr(self, usr, pwd):
        if not self.data.has_key(usr):
            return ERR, "usr not find"

        if self.data[usr] == pwd:
            return OK, "ok"
        else:
            return ERR, "wrong pwd"

g_lm = LoginModule()

class FileModule:
    def __init__(self):
        self.path = "/usr/local/nginx/html/usr_info/"
        self.data = {}
        return

    def app_upload_img(self, usr, files):
        for meta in files:
            outpath = self.path + usr
            with open(outpath, 'wb') as f:
                f.write(meta["body"])

        return OK

    def dev_upload(self, usr, _type, files):
        self.data[usr] = {}
        self.data[usr]["type"] = _type
        self.data[usr]["data"] = files[0]["body"]
        return OK

    def app_download_info(self, usr):
        if self.data.has_key(usr):
            return OK, self.data[usr]
        else:
            return ERR

g_fm = FileModule()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world")

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        usr = self.get_argument('usr')
        pwd = self.get_argument('pwd')

        code, msg = g_lm.check_usr(usr, pwd)
        ret = {
            "code": code,
            "msg": msg,
        }
        self.write(json.dumps(ret))

class AppPushImgHandler(tornado.web.RequestHandler):
    def post(self):
        usr = self.get_argument('usr')
        code = g_fm.app_upload_img(usr, self.request.files["file"])
        ret = {
            "code": code,
        }
        self.write(json.dumps(ret))

class DevPushHandler(tornado.web.RequestHandler):
    def post(self):
        usr = self.get_argument('usr')
        _type = self.get_argument('type')
        code = g_fm.dev_upload(usr, _type, self.request.files["file"])
        ret = {
            "code": code,
        }
        self.write(json.dumps(ret))

class AppGetInfoHandler(tornado.web.RequestHandler):
    def get(self):
        usr = self.get_argument('usr')
        code, data = g_fm.app_download_info(usr)
        ret = {
            "code": code,
            "data": data,
        }
        self.write(json.dumps(ret))

def app_init():
    handlers = [
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/app_push_img", AppPushImgHandler),
        (r"/app_get_info", AppGetInfoHandler),
        (r"/dev_push", DevPushHandler),
    ]

    return tornado.web.Application(
        handlers=handlers,
        debug=True,
    )

if __name__ == "__main__":
    app = app_init()
    app.listen(srv_port)
    tornado.ioloop.IOLoop.current().start()
