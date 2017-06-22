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
import matplotlib.image as img
from PIL import Image

class Handler(BaseHTTPRequestHandler):

	def red_dot (self, x, y):
		image = img.imread('./originalMap.png')

		if(x > 399 or x < 0 or y > 399 or y <0):
			print('x and y have to be between 0 et 399')
			return
		else:
			for i in range(3):
				for j in range (3):
					if(i+x < 400):
						if(y+j < 400):
							image[i+x,y+j,0]=1
							image[i+x,y+j,1]=0
							image[i+x,y+j,2]=0
						if(y-j > -1):
							image[i+x,y-j,0]=1
							image[i+x,y-j,1]=0
							image[i+x,y-j,2]=0
					
					if(x-i > -1):
						if(y+j < 400):
							image[x-i,y+j,0]=1
							image[x-i,y+j,1]=0
							image[x-i,y+j,2]=0
						if(y-j > -1):
							image[x-i,y-j,0]=1
							image[x-i,y-j,1]=0
							image[x-i,y-j,2]=0
			img = Image.fromarray(image, 'RGB')
			img.save('outputMap.jpg')

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

		self.red_dot(295,105)

		with open("outputMap.jpg", "rb") as image_file:
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
