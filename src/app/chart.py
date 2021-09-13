import click
import os
import shutil
import csv
import plotly.graph_objects as go
import pandas as pd

# app-source
import oanda
import common

OUTPUT_DIRECTORY = 'output'
CSV_DIRECTORY = OUTPUT_DIRECTORY + '/oanda_csv'
IMG_DIRECTORY = OUTPUT_DIRECTORY + '/oanda_img'

@click.command()
@click.argument('method', default=None)
@click.option('--account', '-a', default=None)
@click.option('--instruments', '-i', default="EUR_USD,GBP_USD")
@click.option('--granularity', '-g', default='M15')
@click.option('--count', '-c', default='10')
@click.option('--charts', '-p', default='true')
@click.option('--options', '-o', default='data_visible')
def main(method, account, instruments, granularity, count, charts, options):
    instruments = instruments.strip()
    if(instruments == 'all'):
        account = common.fill_account(account)
        instruments = oanda.get_name_instruments(account)
    if(method == 'load_data'):
        load_data(instruments, granularity, count, charts, options)
    if(method == 'clear_output'):
        clear_output()
    return

def load_data(instruments, granularity, count, charts, options):
    for instrument in instruments:
        instrument = instrument.strip()
        load_instrument(instrument, granularity, count, charts, options)
    return

def load_instrument(instrument, granularity, count, charts, options):
    create_dir(CSV_DIRECTORY, IMG_DIRECTORY)
    candles = oanda.get_candles(instrument, count, granularity)
    if(candles == None):
        print('no candles: ' + instrument)
        return
    headers = ['time', 'open', 'high', 'low', 'close', 'volume','type']
    file_path = CSV_DIRECTORY + '/' + instrument + '_data.csv'
    with open(file_path, mode='w') as csv_file:
        csv_file_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_file_writer.writerow(headers)
        for c in candles:
            csv_file_writer.writerow([c.time, str(c.mid.get('o')), str(c.mid.get('h')), str(c.mid.get('l')), str(c.mid.get('c')),
            str(c.volume), c.getType()])
    if(options == 'no_chart'):
        return
    df = pd.read_csv(file_path)
    fig = go.Figure(data=[go.Candlestick(x=df['time'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'])])
    data_visible = (options == 'data_visible')
    fig.update_layout(xaxis_rangeslider_visible=data_visible)
    fig.update_layout(showlegend=data_visible)
    fig.update_xaxes(visible=data_visible)
    fig.update_yaxes(visible=data_visible) 
    image_path = IMG_DIRECTORY + '/' + instrument + '_image.png'
    if charts == 'true':
        fig.write_image(image_path)   
    print(
         'instrument: ' + instrument + 
         ' granularity: ' + granularity +
         ' count: ' + count +
         ', loaded.')
    return 

def clear_output():
    shutil.rmtree(OUTPUT_DIRECTORY)
    print('clear_output completed')
    return

def create_dir(*paths):
    for path in paths:
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            print('directory created: ' + path)
    return

if __name__ == '__main__':
    main()