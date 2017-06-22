import argparse
import socket
import time
import random
import os, sys
import json
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import urllib
from random import randint
import time
from datetime import datetime
import base64

class Handler(BaseHTTPRequestHandler):


	def do_POST(self):
		self.send_response(200)
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Content-Type', 'application/json')
		self.end_headers()
		#print self.rfile.read(int(self.headers['Content-Length']))
		requestJson = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
		print "Recieved message: "
		#print requestJson

		g = open("out.jpg", "w")
		g.write(base64.decodestring(requestJson["image"]))
		g.close()

		with open("out2.jpg", "rb") as image_file:
			encoded_image = base64.b64encode(image_file.read())

		# responseJSON = {"image": encoded_image}
		# responseStr = json.dumps(responseJSON)
		responseStr = encoded_image

		self.wfile.write(responseStr)
		# self.wfile.write('\n')
		return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':

	server = ThreadedHTTPServer(('', 8081), Handler)
	print 'Starting server, use <Ctrl-C> to stop'
	server.serve_forever()
