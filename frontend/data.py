import random
import pandas as pd
import pandas.io.data as web

all_data = {}
for ticker in ['HPQ', 'TSLA', 'YHOO', 'RHT']:
    all_data[ticker] = web.get_data_yahoo(ticker, '1/1/2012', '1/1/2015')
    
price = pd.DataFrame({tic: data['Adj Close'] for tic, data in all_data.iteritems()})
