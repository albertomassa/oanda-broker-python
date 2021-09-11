
import click
import json

# app-source
from model import Trade
import common
import oanda

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
    account = common.fill_account(account)
    url = common.get_property('OANDAResources', 'broker.resources.trades.open').replace('$ACCOUNT_ID$', account)
    response = oanda.get(url)
    trades = response.get('trades')
    if(trades == None):
        print('no trades with account: ' + account)
        return
    headers = [
        {'name': 'Id', 'justify': 'left', 'style': 'cyan'},
        {'name': 'Instrument', 'justify': 'left', 'style': ''},
        {'name': 'Units', 'justify': 'left', 'style': ''},
        {'name': 'Price', 'justify': 'left', 'style': ''},
        {'name': 'Take Profit', 'justify': 'left', 'style': ''},
        {'name': 'Stop Loss', 'justify': 'left', 'style': ''},
        {'name': 'Unrealized PL', 'justify': 'left', 'style': ''},
        {'name': 'State', 'justify': 'left', 'style': ''}
    ]
    rows = []
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
        rows.append([
            t.id,
            t.instrument,
            t.initialUnits,
            t.price,
            take_profit,
            stop_loss,
            t.unrealizedPL, 
            t.getState()])
    common.print_table('Trades List', headers, rows)
    return

def close(account, trade):
    account = common.fill_account(account)
    if(trade == None):
        print('You must specify trade_id')
        return
    trade = trade.strip()
    url = common.get_property('OANDAResources','broker.resources.trades.close').replace('$ACCOUNT_ID$', account).replace('$TRADE_ID$',trade)
    oanda.put(url)
    print('Trade ' + trade + ', closed.')
    return

def stop(account, state):
    account = common.fill_account(account)
    if(state != None):
        state = state.strip()
    url = common.get_property('OANDAResources','broker.resources.trades.open').replace('$ACCOUNT_ID$', account)
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