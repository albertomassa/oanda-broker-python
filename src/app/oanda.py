
import requests
from requests.structures import CaseInsensitiveDict
import configparser

config = configparser.ConfigParser()
config.read('src/ConfigFile.properties')
broker_url = config['OANDABroker']['broker.url']
api_token = config['OANDABroker']['broker.api-token']

headers = CaseInsensitiveDict()
headers['Accept'] = 'application/json'
headers['Authorization'] = 'Bearer ' + api_token

def get(resource_url):    
    return requests.get(broker_url + resource_url, headers=headers).json()

def post(resource_url, body=None):
    # todo
    return

def put(resource_url, body=None):
    return requests.put(broker_url + resource_url, headers=headers).json()

def delete(resource_url, body=None):
    #todo
    return