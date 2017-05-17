import os.path, sys
import logging
import json

from arghandler import ArgumentHandler, subcmd

import config
import upload

logger = logging.getLogger(os.path.basename(__file__))

def context_to_config(context):
    cinfo = Config( host=context.host,
                    port=context.port,
                    username=context.username,
                    password=context.password)

    return cinfo

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

    upload.send_text(args.notebook,args.title,text_content,None,context_to_config(context))

@subcmd(help='send an image block to the server')
def img(parser,context,args):
    parser.add_argument('notebook')
    parser.add_argument('title')
    parser.add_argument('image')

    args = parser.parse_args(args)

    upload.send_image_file(args.notebook,args.title,args.image,None,context_to_config(context))

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

    upload.send_html(args.notebook,args.title,html_content,None,context_to_config(context))

#####
# Main function
def main():
    
    # load basic config info
    config_info = config.load_default_config_info()

    # run the program
    handler = ArgumentHandler('enchant',use_subcommand_help=True)
    handler.set_logging_argument('-L')
    handler.add_argument('-H','--host',default=config_info.host,
                         help='the host for the enchant server')
    handler.add_argument('-P','--port',type=int,default=config_info.port,
                         help='the port for the enchant server')
    handler.add_argument('-u','--user',default=config_info.username,help='the username to use')
    handler.add_argument('-p','--password',default=config_info.password,help='the password to use')

    handler.run()

if __name__ == '__main__':
    main()
