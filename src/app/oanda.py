
import requests
from requests.structures import CaseInsensitiveDict
import configparser
import json

from model import Instrument, CandleStick

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

def getCandles(instrument, count, granularity):
    instrument = instrument.strip()
    url = config['OANDAResources']['broker.resources.candles'].replace('$INSTRUMENT_ID$', instrument)
    count = count.strip()
    url += '?count=' + count
    granularity = granularity.strip()
    url += '&granularity=' + granularity
    response = get(url)
    candles = response.get('candles')
    if(candles == None):
        print('no candles for query')
        return None
    list = []
    for candle in candles:
        c = CandleStick(json.dumps(candle))
        list.append(c)
    return list

def getInstruments(account):
    url = config['OANDAResources']['broker.resources.instruments'].replace('$ACCOUNT_ID$', account)
    response = get(url)
    instruments = response.get('instruments')
    if(instruments == None):
        print('no instruments with account: ' + account)
        return None
    list = []
    for instrument in instruments:
        i = Instrument(json.dumps(instrument))
        list.append(i)
    return list