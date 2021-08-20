import json
import click
import configparser
from model import Account

from rich.console import Console
from rich.table import Table

# app-code
import oanda
from common import fillAccount

config = configparser.ConfigParser()
config.read('src/ConfigFile.properties')

@click.command()
@click.argument('method')
@click.option('--account', '-a', default=None)
@click.option('--options', '-o', default=None)
def main(method, options, account):
    if(method == 'list'):
        accounts()
    if(method == 'details-primary'):
        account_details(account)
    return

def accounts():
    url = config['OANDAResources']['broker.resources.accounts']
    response = oanda.get(url)
    accounts = response.get('accounts')
    console = Console()
    table = Table(title='Accounts List')
    table.add_column('Id', justify='left', style='cyan', no_wrap=True)
    table.add_column('Primary', justify='left', no_wrap=True)
    for account in accounts:
        a = Account(json.dumps(account))
        primary = config['OANDABroker']['broker.account-primary'] == a.id
        table.add_row(
            a.id, 
            str(primary))
    console.print(table)
    return 

def account_details(account):
    account = fillAccount(account)
    url = config['OANDAResources']['broker.resources.accounts'] + '/' + account
    response = oanda.get(url)
    account_dto = response.get('account')
    if(account_dto == None):
        print('no account with id: ' + account)
        return
    a = Account(json.dumps(account_dto))
    console = Console()
    table = Table(title='Account Details')
    table.add_column('Id', justify='left', style='cyan')
    table.add_column('Alias', justify='left')
    table.add_column('Currency', justify='left')
    table.add_column('Balance', justify='left')
    table.add_column('Open Trade Count', justify='left')
    table.add_column('Open Position Count', justify='left')
    table.add_row(
        str(a.id),
        str(a.alias),
        str(a.currency),
        str(a.balance),
        str(a.openTradeCount),
        str(a.openPositionCount))
    console.print(table)
    return

if __name__ == '__main__':
    main()