from flask import Flask, render_template, request, redirect
from flask import Flask
import requests

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
	return requests.get(url).json();



@app.route('/handle_ticker', methods=['POST'])
def handle_ticker():
	ticker = request.form['stock_ticker']
	response = getData(ticker);

	return render_template('index.html', result=response);

if __name__ == '__main__':
  app.run(port=33507)
