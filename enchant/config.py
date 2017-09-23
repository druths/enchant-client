import os, os.path
import json

DEFAULT_CONFIG_FILE = os.path.join(os.environ['HOME'],'.config','enchant.json')

def load_default_config_info():
    cinfo = Config()
    
    if os.path.exists(DEFAULT_CONFIG_FILE):
        cinfo.load_json_config(DEFAULT_CONFIG_FILE)

    return cinfo

######
# Config class
class Config:

    def __init__(self,**kwargs):
        self._host = kwargs.pop('host','127.0.0.1')
        self._port = kwargs.pop('port',13105)
        self._username = kwargs.pop('username',os.environ['USER'])
        self._password = kwargs.pop('password','')

        if len(kwargs) > 0:
            raise Exception, 'unknown arguments: %s' % ','.join(kwargs.keys())

    def load_json_config(self,fname):
        config_data = json.load(open(fname,'r'))

        self._host = config_data.get('host',self._host)
        self._port = config_data.get('port',self._port)
        self._username = config_data.get('username',self._username)
        self._password = config_data.get('password',self._password)

    def write_json_config(self,fname):
        json.dump( {
                        'host': self._host,
                        'port': self._port,
                        'username': self._username,
                        'password': self._password
                    },open(fname,'w'))

        return

    def __getattr__(self,name):
        if name == 'host':
            return self._host
        elif name == 'port':
            return self._port
        elif name == 'username':
            return self._username
        elif name == 'password':
            return self._password
        else:
            raise Exception,'no attribute: %s' % name

        
##########
# Local configuration

LOCAL_CONFIGFILE_NAME = '.enchant'

def find_local_config_file(path=None):

    if path is None:
        path = os.getcwd()

    has_config = lambda x: os.path.exists(os.path.join(x,LOCAL_CONFIGFILE_NAME))

    # find the first configfile we encounter on our walk to the root
    last_path = path
    while not (path == last_path or has_config(path)):
        last_path = path
        path = os.path.dirname(path)

    # open it, if we found it
    if has_config(path):
        return os.path.join(path,LOCAL_CONFIGFILE_NAME)
    else:
        return None

def load_local_config(path=None):
    
    if path is None:
        path = os.getcwd()

    local_config = LocalConfig()

    config_file = find_local_config_file(path)

    # open it, if we found it
    if config_file is not None:
        local_config.load_json_config(config_file)

    return local_config

class LocalConfig:

    def __init__(self,**kwargs):
        self._notebook = kwargs.pop('notebook',None)

        if len(kwargs) > 0:
            raise Exception, 'unexpected arguments: %s' % kwargs.keys()

    def load_json_config(self,fname):
        config_info = json.load(open(fname,'r'))

        self._notebook = config_info.get('notebook',None)

    def write_json_config(self,fname):
        data = {}
        if self._notebook is not None:
            data['notebook'] = self._notebook

        json.dump(data, open(fname,'w'))

    def __getattr__(self,name):
        if name == 'notebook':
            return self._notebook
        else:
            raise Exception,'no attribute: %s' % name

