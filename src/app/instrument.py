
import click
import configparser
import json

from rich.console import Console
from rich.table import Table

# app-code
from model import CandleStick, Instrument
from common import fillAccount
import oanda

config = configparser.ConfigParser()
config.read('src/ConfigFile.properties')

@click.command()
@click.argument('method', default=None)
@click.option('--account', '-a', default=None)
@click.option('--instrument', '-i', default=None)
@click.option('--count', '-c', default='10')
@click.option('--granularity', '-g', default='M15')
@click.option('--options', '-o', default=None)
def main(method, account, instrument, count, granularity, options):
    if(method == 'list'):
       instruments(account) 
    if(method == 'candles'):
       candles(instrument, count, granularity)
    return

def instruments(account):
    account = fillAccount(account)
    url = config['OANDAResources']['broker.resources.instruments'].replace('$ACCOUNT_ID$', account)
    response = oanda.get(url)
    instruments = response.get('instruments')
    if(instruments == None):
        print('no instruments with account: ' + account)
        return
    console = Console()
    table = Table(title='Instruments List')
    table.add_column('Name', justify='left', style='cyan',)
    table.add_column('Type', justify='left')
    table.add_column('Display Name', justify='left')    
    for instrument in instruments:
        i = Instrument(json.dumps(instrument))
        table.add_row(
            i.name,
            i.type,
            i.displayName)    
    console.print(table)
    return

def candles(instrument, count, granularity):
    if(instrument == None):
        print('no instrument specified')
        return
    else:
        instrument = instrument.strip()
    url = config['OANDAResources']['broker.resources.candles'].replace('$INSTRUMENT_ID$', instrument)
    if(count != None):
        count = count.strip()
    url += '?count=' + count
    if(granularity != None):
        granularity = granularity.strip()
    url += '&granularity=' + granularity
    response = oanda.get(url)
    if(granularity == None):
        granularity = response.get('granularity')
    candles = response.get('candles')
    if(candles == None):
        print('no candles for query')
        return
    console = Console()
    table = Table(title='Instrument Params')
    table.add_column('Instrument', justify='left', style='cyan')
    table.add_column('Granularity', justify='left')
    table.add_column('Count', justify='left')
    table.add_row(
        instrument,
        granularity,
        count
    )
    console.print(table)
    table = Table(title='Candles')
    table.add_column('Number', justify='left', style='cyan')
    table.add_column('Instrument', justify='left')
    table.add_column('Granularity', justify='left')
    table.add_column('Time', justify='left')
    table.add_column('Complete', justify='left')
    table.add_column('Open', justify='left')    
    table.add_column('High', justify='left')  
    table.add_column('Low', justify='left')  
    table.add_column('Close', justify='left')  
    table.add_column('Volume', justify='left')  
    table.add_column('Type', justify='left')
    number = 1
    for candle in candles:
        c = CandleStick(json.dumps(candle))
        table.add_row(
            str(number),
            instrument,
            granularity,
            c.time,
            str(c.complete),
            str(c.mid.get('o')),
            str(c.mid.get('h')),
            str(c.mid.get('l')),
            str(c.mid.get('c')),
            str(c.volume), 
            c.getType())
        number += 1
    console.print(table)
    return
    
if __name__ == '__main__':
    main()