# -*- coding: utf-8 -*-
import SimpleHTTPServer
import SocketServer
import json
# from requests_toolbelt.multipart import decoder
import urllib

import os
ON_HEROKU = os.environ.get('ON_HEROKU')

import re
import sys

from instapy_cli.__main__ import main as damain

def instapy(params):
    # sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.argv[0]=params
    return damain(params)


PORT = 8000

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_POST(self):

        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        username=""
        password=""
        imagen=""
        caption=""
        # parsed_body= post_body.split("&"):
        # parsed_body[0].split("=").[0]
        for pares in  post_body.split("&"):
            if pares.split("=")[0]=="username":
                username=pares.split("=")[1]
            if pares.split("=")[0]=="password":
                password=pares.split("=")[1]
            # urlencode(imagen)
            if pares.split("=")[0]=="imagen":
                imagen=pares.split("=")[1]
                imagen= urllib.unquote(imagen).decode('utf8')
            if pares.split("=")[0]=="caption":
                caption=pares.split("=")[1]
                caption = caption.replace('+',' ').replace('%0A', '\n')
        instapy(["-u", username, "-p",password,"-f",imagen, "-t", caption])
        # print self.get_route()
        self.send_response(200)




Handler = ServerHandler

if ON_HEROKU:
    httpd = SocketServer.TCPServer(("", int(os.environ.get('PORT'))), Handler)
    print "serving"
else:
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print "serving at port", PORT


try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print('Stopping HTTP server')
    httpd.server_close()
