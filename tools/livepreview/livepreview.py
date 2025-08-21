#!/usr/bin/env python3

import os
import sys
import glob
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8888
SERVER_LOCAL_PATH = Path(__file__).resolve().parent
PREVIEW_TEMPLATE  = os.path.join(SERVER_LOCAL_PATH, 'preview.html')
STATIC_TEMPLATE   = os.path.join(SERVER_LOCAL_PATH, 'shader-static.js')
ANIMATED_TEMPLATE = os.path.join(SERVER_LOCAL_PATH, 'shader-animated.js')

class MyRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            file_path = self.path[1:]

            if self.path.endswith('.txt') or self.path.endswith('.html'):
                f = open(file_path, 'rb') 
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Content-length', os.path.getsize(file_path))
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            elif self.path.endswith('.txt.static') or self.path.endswith('.txt.animated'):
                js_template = STATIC_TEMPLATE
                if self.path.endswith('.txt.animated'):
                    js_template = ANIMATED_TEMPLATE

                f_preview = open(PREVIEW_TEMPLATE, 'rb') 
                f_js_template = open(js_template, 'rb')
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f_preview.read())
                self.wfile.write(f_js_template.read())

                f_preview.close()
                f_js_template.close()
                return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)


# Create the HTTP server and run it
server_url = 'http://127.0.0.1:%s' % PORT

# By default serve scripts form livepreview directory
serving_directory = SERVER_LOCAL_PATH

if len(sys.argv) > 1:
    if sys.argv[1] == '--current':
        serving_directory = os.getcwd()
    else:
        serving_directory = sys.argv[1]

os.chdir(serving_directory)

print("Server path:       %s" % SERVER_LOCAL_PATH)
print("Preview template:  %s" % PREVIEW_TEMPLATE)
print("Static template:   %s" % STATIC_TEMPLATE)
print("Animated template: %s" % ANIMATED_TEMPLATE)
print("Serving from:      %s" % serving_directory)
print("Local server at:   %s" % server_url)
print("")
for f in glob.glob('*.txt'):
    print('%s/%s.static' % (server_url, f))
    print('%s/%s.animated' % (server_url, f))

server = HTTPServer(('', 8888), MyRequestHandler)
server.serve_forever()
