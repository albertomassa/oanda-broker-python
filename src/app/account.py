import json
import click
import configparser

# app-source
import oanda
import common
from model import Account

@click.command()
@click.argument('method')
@click.option('--account', '-a', default=None)
@click.option('--options', '-o', default=None)
def main(method, account, options):
    if(method == 'list'):
        accounts()
    if(method == 'details-primary'):
        account_details(account)
    return

def accounts():
    url = common.get_property('OANDAResources', 'broker.resources.accounts')
    response = oanda.get(url)
    accounts = response.get('accounts')
    headers = [
        {'name': 'Id', 'justify': 'left', 'style': 'cyan'},
        {'name': 'Primary', 'justify': 'left', 'style': ''}
    ]
    rows = []
    for account in accounts:
        a = Account(json.dumps(account))
        primary = common.get_property('OANDABroker', 'broker.account-primary') == a.id
        rows.append([a.id,str(primary)])
    common.print_table('Account List', headers, rows)
    return 

def account_details(account):
    account = common.fill_account(account)
    url = common.get_property('OANDAResources','broker.resources.accounts') + '/' + account
    response = oanda.get(url)
    account_dto = response.get('account')
    if(account_dto == None):
        print('no account with id: ' + account)
        return
    a = Account(json.dumps(account_dto))
    headers = [
        {'name': 'Id', 'justify': 'left', 'style': 'cyan'},
        {'name': 'Alias', 'justify': 'left', 'style': ''},
        {'name': 'Currency', 'justify': 'left', 'style': ''},
        {'name': 'Balance', 'justify': 'left', 'style': ''},
        {'name': 'Open Trade Count', 'justify': 'left', 'style': ''},
        {'name': 'Open Position Count', 'justify': 'left', 'style': ''},
    ]
    rows = []
    rows.append([
        str(a.id),
        str(a.alias),
        str(a.currency),
        str(a.balance),
        str(a.openTradeCount),
        str(a.openPositionCount)])
    common.print_table('Account Details', headers, rows)
    return

if __name__ == '__main__':
    main()