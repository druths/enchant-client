import os.path
import logging
import json
import requests
import datetime

from . import config

logger = logging.getLogger(os.path.basename(__file__))

def config_to_url(config_info):
    return 'http://%s:%d' % (config_info.host,config_info.port)

def get_current_time():
    return datetime.datetime.now().strftime('%b %d, %Y %H:%M')

def make_base_header(config_info,title,timestamp):
    if timestamp is None:
        timestamp = get_current_time()

    return {'username':config_info.username, 'password':config_info.password,'title':title,'timestamp':timestamp}

#########
# functions

def handle_result(result_content):
    try:
        result = json.loads(result_content)
        if result['result'] != 'ok':
            logger.error('upload failed. server reported error type=%s, with message: %s' % (result['result'],result['message']))             
    except:
        logger.exception('upload failed with exception')

def send_text(notebook,title,content,timestamp=None,config_info=None):
    if config_info is None:
        config_info = config.load_default_config_info()

    headers = {'Content-Type': 'text/plain'}

    header_dict = make_base_header(config_info,title,timestamp)
    full_content = '%s\n%s' % (json.dumps(header_dict),content)

    complete_url = '%s/submit/text/%s/%s' % (config_to_url(config_info),config_info.username,notebook)
    r = requests.post(complete_url,data=full_content,headers=headers)

    handle_result(r.text)

def send_html(notebook,title,content,timestamp=None,config_info=None):
    if config_info is None:
        config_info = config.load_default_config_info()

    complete_url = '%s/submit/html/%s/%s' % (config_to_url(config_info),config_info.username,notebook)
    
    header_dict = make_base_header(config_info,title,timestamp)

    files = {'file': content}

    r = requests.post(complete_url,data=header_dict,files=files) #,headers=headers)

    handle_result(r.text)

def send_image_file(notebook,title,image_filename,timestamp=None,config_info=None):
    if config_info is None:
        config_info = config.load_default_config_info()
    
    complete_url = '%s/submit/image/%s/%s' % (config_to_url(config_info),config_info.username,notebook)

    header_dict = make_base_header(config_info,title,timestamp)

    files = {'file': open(image_filename,'rb')}

    r = requests.post(complete_url,data=header_dict,files=files)

    handle_result(r.text)

