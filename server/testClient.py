import socket
import time
import requests
import urllib
import httplib
import socket
import uuid
import json
import base64


class Client(object):

	def __init__(self):
		# self.send_requests()
		self.send_image()

	def send_json_to_server(self,host, port, jsonObj):
		jsonStr = json.dumps(jsonObj)
		headers = {"Content-type": "application/json", "Accept": "application/json"}
		conn = httplib.HTTPConnection(host + ":" + str(port))
		conn.request("POST","/",jsonStr, headers)
		response = conn.getresponse().read()
		return json.loads(response)

	def send_image(self):

		host = "127.0.0.1"
		with open("test.png", "rb") as image_file:
			encoded_image = base64.b64encode(image_file.read())

		sendJson = {"image": encoded_image}

		responseJson = self.send_json_to_server(host,8080, sendJson)
		print responseJson["sysResponse"]


	def send_requests(self):

		while True:
			data = raw_input("Please enter your question or enter \"disconnect\" to exit: ")
			if data == "disconnect":
				print "Disconnecting"
				self.client_socket.send("disconnect")
				self.client_socket.close()
				break
			else:
				print 'send to server: ' + data
				# host = "ec2-52-90-114-249.compute-1.amazonaws.com"
				host = "127.0.0.1"

				sendJson = {"message": data}
				responseJson = self.send_json_to_server(host,8080, sendJson)
				print responseJson["sysResponse"]

if __name__ == "__main__":
	client = Client()