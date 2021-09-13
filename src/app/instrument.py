
import click

# app-source
from common import fill_account, print_table
import oanda

@click.command()
@click.argument('method', default=None)
@click.option('--account', '-a', default=None)
@click.option('--instrument', '-i', default="EUR_USD")
@click.option('--granularity', '-g', default='M15')
@click.option('--count', '-c', default='10')
@click.option('--options', '-o', default=None)
def main(method, account, instrument, granularity, count, options):
    if(method == 'list'):
       instruments(account) 
    if(method == 'candles'):
       candles(instrument, granularity, count)
    return

def instruments(account):
    account = fill_account(account)
    instruments = oanda.get_instruments(account)
    if(instruments == None): 
        return
    headers = [
        {'name': 'Name', 'justify': 'left', 'style': 'cyan'},
        {'name': 'Type', 'justify': 'left', 'style': ''},
        {'name': 'Display name', 'justify': 'left', 'style': ''},
    ]
    rows = []
    for i in instruments:
        rows.append([i.name, i.type, i.displayName])
    print_table('Instrument List', headers, rows)
    return

def candles(instrument, granularity, count):
    candles = oanda.get_candles(instrument, count, granularity)
    if(candles == None):
        return
    headers = [
        {'name': 'Instrument', 'justify': 'left', 'style': 'cyan'},
        {'name': 'Granularity', 'justify': 'left', 'style': ''},
        {'name': 'Count', 'justify': 'left', 'style': ''},
    ]
    rows = []
    rows.append([instrument, granularity, count])
    print_table('Instrument Params', headers, rows) # print_params_table
    headers = [
        {'name': 'Number', 'justify': 'left', 'style': 'cyan'},
        {'name': 'Instrument', 'justify': 'left', 'style': ''},
        {'name': 'Granularity', 'justify': 'left', 'style': ''},
        {'name': 'Time', 'justify': 'left', 'style': ''},
        {'name': 'Complete', 'justify': 'left', 'style': ''},
        {'name': 'Open', 'justify': 'left', 'style': ''},
        {'name': 'High', 'justify': 'left', 'style': ''},
        {'name': 'Low', 'justify': 'left', 'style': ''},
        {'name': 'Close', 'justify': 'left', 'style': ''},
        {'name': 'Volume', 'justify': 'left', 'style': ''},
        {'name': 'Type', 'justify': 'left', 'style': ''}
    ]
    rows = []
    number = 1
    for c in candles:
        rows.append([
            str(number),instrument,granularity,c.time,str(c.complete),
            str(c.mid.get('o')),str(c.mid.get('h')),str(c.mid.get('l')),str(c.mid.get('c')),
            str(c.volume), c.getType()])
        number += 1
    print_table('Candles', headers, rows) # print_candles_table
    return

if __name__ == '__main__':
    main()