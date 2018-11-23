import os.path, sys
import logging
import json
import getpass
import subprocess

from arghandler import ArgumentHandler, subcmd
import argparse

from . import config
from . import upload

logger = logging.getLogger(os.path.basename(__file__))

def context_to_config(context):
    cinfo = config.Config(  host=context.host,
                            port=context.port,
                            username=context.username,
                            password=context.password)

    return cinfo

@subcmd(help='configure local settings')
def local_config(parser,context,args):
    parser.add_argument('-F','--force',action='store_true',
                        help='force the creation of a local settings file in the current directory')
    args = parser.parse_args(args)

    local_config_filepath = config.find_local_config_file()
   
    if local_config_filepath is not None:
        if args.force is False:
            logger.error('use -F flag to override local config file at: %s' % local_config_filepath)
        else:
            logger.warn('overriding local config file at: %s' % local_config_filepath)

    # get the config info
    notebook = raw_input('notebook: ')

    # write the new config info
    local_config = config.LocalConfig(notebook=notebook)
    local_config.write_json_config(os.path.join(os.getcwd(),config.LOCAL_CONFIGFILE_NAME))

    # done!

@subcmd(help='configure global settings')
def global_config(parser,context,args):
    parser.add_argument('-f','--config_file',nargs='?',default=None,
                        help='the configuration file to write settings to')

    args = parser.parse_args(args)

    # build the context
    cfg = None
    if args.config_file is None:
        cfg = context_to_config(context)
    else:
        cfg = config.Config()
        if os.path.exists(args.config_file):
            cfg.load_json_config(args.config_file)
                     
    # prompt for config info
    host = raw_input('host [%s]: ' % cfg.host).strip()
    host = host if len(host) > 0 else cfg.host

    port = raw_input('port [%d]: ' % cfg.port).strip()
    try:
        port = int(port) if len(port) > 0 else cfg.port
    except:
        logger.error('port must be a number')
        exit()


    username = raw_input('username [%s]: ' % cfg.username).strip()
    username = username if len(username) > 0 else cfg.username

    password = getpass.getpass('password: ').strip()
    password = password if len(password) > 0 else cfg.password

    # update the context
    cfg = config.Config(host=host,port=port,username=username,password=password)

    # write the context out
    fname = args.config_file if args.config_file is not None else config.DEFAULT_CONFIG_FILE
    logger.info('writing config info to file: %s' % fname)
    cfg.write_json_config(fname)

@subcmd(help='send a text block to the server')
def txt(parser,context,args):
    local_config = config.load_local_config()

    parser.add_argument('-n','--notebook',required=local_config.notebook is None,default=local_config.notebook)
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
    local_config = config.load_local_config()

    parser.add_argument('-n','--notebook',required=local_config.notebook is None,default=local_config.notebook)
    parser.add_argument('title')
    parser.add_argument('image')

    args = parser.parse_args(args)

    upload.send_image_file(args.notebook,args.title,args.image,None,context_to_config(context))

@subcmd(help='send an html block to the server')
def html(parser,context,args):
    local_config = config.load_local_config()

    parser.add_argument('-n','--notebook',required=local_config.notebook is None,default=local_config.notebook)
    parser.add_argument('title')
    parser.add_argument('content',help='the html to send. if "-", will read text from stdin')

    args = parser.parse_args(args)

    # read the content from stdin if necessary
    html_content = args.content
    if html_content == '-':
        html_content = sys.stdin.read()

    upload.send_html(args.notebook,args.title,html_content,None,context_to_config(context))

@subcmd(help='send the results of an execution task to the server as a text block')
def run(parser,context,args):
    local_config = config.load_local_config()

    parser.add_argument('-n','--notebook',required=local_config.notebook is None,default=local_config.notebook)
    parser.add_argument('-t','--title',required=False,default=None)
    parser.add_argument('cmd',nargs=argparse.REMAINDER)

    args = parser.parse_args(args)

    # run the command
    cmd = ' '.join(args.cmd)
    logger.info('executing command: %s' % cmd)
    output = subprocess.check_output(cmd,shell=True,stderr=subprocess.STDOUT)

    title = args.title if args.title is not None else cmd

    upload.send_text(args.notebook,title,output,config_info=context_to_config(context))

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
    handler.add_argument('-u','--username',default=config_info.username,help='the username to use')
    handler.add_argument('-p','--password',default=config_info.password,help='the password to use')

    handler.run()

if __name__ == '__main__':
    main()
