import os.path
import logging
import json
import requests

logger = logging.getLogger(os.path.basename(__file__))

class ServerInfo:
	def __init__(self,host,port):
		self.host = host
		self.port = port

	def to_url(self):
		return 'http://%s:%d' % (self.host,self.port)

#########
# functions

def handle_result(result_content):
	try:
		result = json.loads(result_content)
		if result['result'] != 'ok':
			logger.error('upload failed with error: %s' % result['result'])				
	except:
		logger.exception('upload failed with exception')

def send_text(server_info,username,notebook,title,timestamp,content):
	headers = {'Content-Type': 'text/plain'}

	header = '{"title":"%s","timestamp":"%s"}' % (title,timestamp)
	full_content = '%s\n%s' % (header,content)

	complete_url = '%s/submit/text/%s/%s' % (server_info.to_url(),username,notebook)
	r = requests.post(complete_url,data=full_content,headers=headers)

	handle_result(r.text)

def send_html(server_info,username,notebook,title,timestamp,content):
	headers = {'Content-Type': 'text/html'}

	header = '{"title":"%s","timestamp":"%s"}' % (title,timestamp)
	full_content = '%s\n%s' % (header,content)

	complete_url = '%s/submit/html/%s/%s' % (server_info.to_url(),username,notebook)
	r = requests.post(complete_url,data=full_content,headers=headers)

	handle_result(r.text)

def send_image_file(server_info,username,notebook,title,timestamp,image_filename):
	complete_url = '%s/submit/image/%s/%s' % (server_info.to_url(),username,notebook)

	header = {'title':title, 'timestamp':timestamp}
	files = {'file': open(image_filename,'rb')}

	r = requests.post(complete_url,data=header,files=files)

	handle_result(r.text)

