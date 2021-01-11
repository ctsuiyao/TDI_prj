from flask import Flask, render_template, request, redirect
from flask import Flask

import requests
import pandas as pd
import numpy as np

from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components


app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

def getData(ticker):
	key = "UV9CGUW2Q0TPZ818"
	url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker, key);
	return requests.get(url);

def convert_response(d):
    # convert the response into datetimerecords that can be
    # parsed by Pandas
    for dt, prec in d['Time Series (Daily)'].items():
        r = { 'datetime': dt}
        r.update(prec)
        yield r
def datetime(x):
    return np.array(x, dtype=np.datetime64)

@app.route('/handle_ticker', methods=['POST'])
def handle_ticker():
	ticker = request.form['stock_ticker']
	response = getData(ticker);
	data = response.json()
	# pass your response 'page'
	df = pd.DataFrame(convert_response(data))
	# rename the columns    
	df = df.rename(columns={ '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. adjusted close': 'AdjClose', '6. volume': 'Volume'})
	df['datetime'] = pd.to_datetime(df['datetime'])
	df.set_index('datetime', inplace=True)
	df.sort_index(inplace=True)
	# extract the columns you want
	df = df[[ 'Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']]
	df2 = df.sort_values(by="datetime", ascending=False)[:30]



	p1 = figure(x_axis_type="datetime", title="Stock Closing Prices")
	p1.grid.grid_line_alpha=0.3
	p1.xaxis.axis_label = 'Date'
	p1.yaxis.axis_label = 'Price'

	p1.line(datetime(df2.index),df2['Close'], color='#A6CEE3', legend_label=ticker);
	p1.legend.location = "top_left"
	script, div = components(p1)

	return render_template('index.html', div=div, script=script);

if __name__ == '__main__':
  app.run(port=33507)
