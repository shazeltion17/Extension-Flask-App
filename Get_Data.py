import numpy as np
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
# from configparser import ConfigParser
import psycopg2
import requests

#cer = '/opt/app/fireanalytics-dev.crt'
#key = '/opt/app/testcert.key'
#bundle = '/opt/app/fireanalyics-dev_tech.ca-bunlde'

#def test_1():
#    r = requests.get('https://github.com',verify=False)
#    print r
#   return

#test_1()



def get_data(symbol, hashvalue):

    # Technical Indicators
    ti = TechIndicators(key='90SI5AD8BUL571ZI', output_format='pandas')
    #sma15, _ = ti.get_sma(symbol=symbol, interval='daily',time_period=15)
    #sma30, _ = ti.get_sma(symbol=symbol, interval='daily', time_period=30)
    sma60, _ = ti.get_sma(symbol=symbol, interval='daily', time_period=60) 	  
    #sma15 = sma15['SMA']
    #sma30 = sma30['SMA']
    sma60 = sma60['SMA']
    #print sma60
    ts = TimeSeries(key='90SI5AD8BUL571ZI', output_format='pandas')
    close = ts.get_daily(symbol=symbol, outputsize='full')[0]['4. close']
    volume = ts.get_daily(symbol=symbol, outputsize='full')[0]['5. volume']
    ticker = pd.Series(np.repeat(symbol, len(sma60), axis=0))
    ticker.name = 'ticker'
    # Find a Target
    # target = (((sma15 - sma15.shift()) / sma15.shift()) < 0) & (((sma30 - sma30.shift()) / sma30.shift()) < 0) & (((sma60 - sma60.shift()) / sma60.shift()) < 0)
    # Create Items in the database
    # target.name = 'target'
    close.name = 'close'
    volume.name = 'volume'
    # sma15.name = 'sma15'
    # sma30.name = 'sma30'
    # sma60.name = 'sma60'
    # data = pd.DataFrame(pd.concat([close, volume, target, sma15, sma30, sma60], axis=1))
    # print ticker
    # print sma60
    data = pd.DataFrame(pd.concat([sma60, close, volume], axis=1, sort=False))
    data['ticker'] = symbol
    data['hash'] = hashvalue
    # print data
    # data['sellsign'] = (data['sma15'] > data['sma30']) & (data['sma15'].shift(-1) < data['sma30'].shift(-1))
    # data['buysign'] = (data['sma15'] < data['sma30']) & (data['sma15'].shift(-1) > data['sma30'].shift(-1))
    # Print to a CSV File
    # print data
    #data.to_csv('C:\Users\sehrlich\Desktop\sam2.csv')
#    print data
    return data


def build_connection():
    conn = psycopg2.connect(host="tableaudatainstance.cotqt9fi7tuv.us-west-2.rds.amazonaws.com", dbname="postgres", user="Samuel", password="thecatranfast")
    cur = conn.cursor()
    # print cur
    return cur, conn


def run_sql(cur, conn, data):
    sql = "INSERT INTO pricing (dateclose, sma, close, volume, ticker, hashvalue) VALUES"
    #print data
    args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s)", x) for x in data)
    cur.execute(sql + args_str)
    conn.commit()
    cur.close()
    conn.close()
    return

# Run this manually

# symbol = 'BAC'
# hashvalue = '1235'
# data = get_data(symbol, hashvalue)
# data = [tuple(x) for x in data.to_records(index=True)]
# cur, conn = build_connection();
# run_sql(cur, conn, data);
#

