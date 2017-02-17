import os.path, sys
import logging
import datetime

from arghandler import ArgumentHandler, subcmd

import upload

logger = logging.getLogger(os.path.basename(__file__))

def get_current_time():
	return datetime.datetime.now().strftime('%b %d, %Y %H:%M')

@subcmd(help='send a text block to the server')
def txt(parser,context,args):
	parser.add_argument('notebook')
	parser.add_argument('title')
	parser.add_argument('content',help='the text to send. if "-", will read text from stdin')

	args = parser.parse_args(args)
		
	# read the content from stdin if necessary
	text_content = args.content
	if text_content == '-':
		text_content = sys.stdin.read()

	server_info = upload.ServerInfo(context.address,context.port)
	upload.send_text(server_info,args.notebook,args.title,get_current_time(),text_content)

@subcmd(help='send an image block to the server')
def img(parser,context,args):
	parser.add_argument('notebook')
	parser.add_argument('title')
	parser.add_argument('image')

	args = parser.parse_args(args)

	server_info = upload.ServerInfo(context.address,context.port)
	upload.send_image_file(server_info,args.notebook,args.title,get_current_time(),args.image)

@subcmd(help='send an html block to the server')
def html(parser,context,args):
	parser.add_argument('notebook')
	parser.add_argument('title')
	parser.add_argument('content',help='the html to send. if "-", will read text from stdin')

	args = parser.parse_args(args)

	# read the content from stdin if necessary
	html_content = args.content
	if html_content == '-':
		html_content = sys.stdin.read()

	server_info = upload.ServerInfo(context.address,context.port)
	upload.send_html(server_info,args.notebook,args.title,get_current_time(),html_content)

#####
# Main function
def main():
	handler = ArgumentHandler('enchant',use_subcommand_help=True)
	handler.set_logging_argument('-L')
	handler.add_argument('-A','--address',default='127.0.0.1',
						 help='the address for the enchant server')
	handler.add_argument('-P','--port',type=int,default=3150,
						 help='the port for the enchant server')

	handler.run()

if __name__ == '__main__':
	main()
