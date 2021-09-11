
import click
import os
import shutil
import csv
import plotly.graph_objects as go
import pandas as pd

# app-source
import oanda

OUTPUT_DIRECTORY = 'output'
CSV_DIRECTORY = OUTPUT_DIRECTORY + '/oanda_csv'
IMG_DIRECTORY = OUTPUT_DIRECTORY + '/oanda_img'

@click.command()
@click.argument('method', default=None)
@click.option('--instrument', '-i', default="EUR_USD")
@click.option('--granularity', '-g', default='M15')
@click.option('--count', '-c', default='10')
@click.option('--options', '-o', default='no_data_visible')
def main(method, instrument, granularity, count, options):
    if(method == 'print_chart'):
        print_chart(instrument, granularity, count, options)
    if(method == 'clear_output'):
        clear_output()
    return

def print_chart(instrument, granularity, count, options):
    create_dir(CSV_DIRECTORY, IMG_DIRECTORY)
    candles = oanda.getCandles(instrument, count, granularity)
    if(candles == None):
        return
    headers = ['time', 'open', 'high', 'low', 'close']
    file_path = CSV_DIRECTORY + '/' + instrument + '_data.csv'
    with open(file_path, mode='w') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(headers)
        for c in candles:
            employee_writer.writerow([c.time, str(c.mid.get('o')),str(c.mid.get('h')),str(c.mid.get('l')),str(c.mid.get('c'))])
    df = pd.read_csv(file_path)
    fig = go.Figure(data=[go.Candlestick(x=df['time'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'])])
    data_visible = options == 'data_visible'
    fig.update_layout(xaxis_rangeslider_visible=data_visible)
    fig.update_layout(showlegend=data_visible)
    fig.update_xaxes(visible=data_visible)
    fig.update_yaxes(visible=data_visible) 
    config = {
        'toImageButtonOptions': {
            'format': 'png', 
            'filename': instrument,
            'height': 500,
            'width': 700,
            'scale': 1 
        },
    }
    fig.show(config=config)
    image_path = IMG_DIRECTORY + '/' + instrument + '_image.png'
    fig.write_image(image_path)   
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