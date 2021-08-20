
import click
import configparser
import json

from rich.console import Console
from rich.table import Table

# app-code
from model import Trade
from common import fillAccount
import oanda

config = configparser.ConfigParser()
config.read('src/ConfigFile.properties')

@click.command()
@click.argument('method', default=None)
@click.option('--account', '-a', default=None)
@click.option('--trade', '-t', default=None)
@click.option('--state', '-s', default=None)
@click.option('--options', '-o', default=None)
def main(method, account, trade, state, options):
    if(method == 'list'):
        trades(account)
    if(method == 'close'):
        close(account,trade)
    if(method == 'stop'):
        stop(account, state)
    return

def trades(account):
    account = fillAccount(account)
    url = config['OANDAResources']['broker.resources.trades.open'].replace('$ACCOUNT_ID$', account)
    response = oanda.get(url)
    trades = response.get('trades')
    if(trades == None):
        print('no trades with account: ' + account)
        return
    console = Console()
    table = Table(title='Trade Params')
    table.add_column('Account', justify='left', style='cyan')
    table.add_row(
        account)
    console.print(table)
    table = Table(title='List Trades')
    table.add_column('Id', justify='left')
    table.add_column('Instrument', justify='left', style='cyan')
    table.add_column('Units', justify='left')
    table.add_column('Price', justify='left')
    table.add_column('Take Profit', justify='left')
    table.add_column('Stop Loss', justify='left')
    table.add_column('Unrealized PL', justify='left')
    table.add_column('State', justify='left')
    for trade in trades:
        t = Trade(json.dumps(trade))
        if(trade.get('takeProfitOrder') != None):
            take_profit = t.takeProfitOrder.get('price')
        else:
            take_profit = 'None'
        if(trade.get('stopLossOrder') != None):
            stop_loss = t.stopLossOrder.get('price')
        else:
            stop_loss = 'None'
        table.add_row(
            t.id,
            t.instrument,
            t.initialUnits,
            t.price,
            take_profit,
            stop_loss,
            t.unrealizedPL, 
            t.getState())
    console.print(table)
    return

def close(account, trade):
    account = fillAccount(account)
    if(trade == None):
        print('You must specify trade_id')
        return
    trade = trade.strip()
    url = config['OANDAResources']['broker.resources.trades.close'].replace('$ACCOUNT_ID$', account).replace('$TRADE_ID$',trade)
    oanda.put(url)
    print('Trade ' + trade + ', closed.')
    return

def stop(account, state):
    account = fillAccount(account)
    if(state != None):
        state = state.strip()
    url = config['OANDAResources']['broker.resources.trades.open'].replace('$ACCOUNT_ID$', account)
    response = oanda.get(url)
    trades = response.get('trades')
    ids = []
    for trade in trades:
        t = Trade(json.dumps(trade))
        if(state != None and state == t.getState()):
            ids.append(t.id)
        elif(state == None):
            ids.append(t.id)
    for id in ids:
        close(account, id)
    return

if __name__ == '__main__':
    main()