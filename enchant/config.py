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

        
        
