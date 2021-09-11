
import configparser
from rich.console import Console
from rich.table import Table

config = configparser.ConfigParser()
config.read('src/ConfigFile.properties')

def get_property(resource, name):    
    return config[resource][name]

def fill_account(account):
    if(account == None):
        account = get_property('OANDABroker', 'broker.account-primary')
    else:
        account = account.strip()   
    return account

def print_table(title, headers, rows): 
    if(title == None or headers == None or rows == None):
        print('wrong params')
        return
    console = Console()
    table = Table(title=title)
    for h in headers:
        table.add_column(h.get('name'), justify=h.get('justify'), style=h.get('style'))
    if(rows != None):
        for r in rows:
            table.add_row(*r)
    console.print(table)
    return 

