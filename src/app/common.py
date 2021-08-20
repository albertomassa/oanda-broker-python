
import configparser

config = configparser.ConfigParser()
config.read('src/ConfigFile.properties')

def fillAccount(account):
    if(account == None):
        account = config['OANDABroker']['broker.account-primary']
    else:
        account = account.strip()   
    return account