import httplib
import urllib

try: import simplejson as json
except ImportError: import json

PUBLIC_API_URL = 'http://query.yahooapis.com/v1/public/yql'
DATATABLES_URL = 'store://datatables.org/alltableswithkeys'
HISTORICAL_URL = 'http://ichart.finance.yahoo.com/table.csv?s='
RSS_URL = 'http://finance.yahoo.com/rss/headline?s='
FINANCE_TABLES = {'quotes': 'yahoo.finance.quotes',
                 'options': 'yahoo.finance.options',
                 'quoteslist': 'yahoo.finance.quoteslist',
                 'sectors': 'yahoo.finance.sectors',
                 'industry': 'yahoo.finance.industry'}


def execute_yql_query(yql):
    conn = httplib.HTTPConnection('query.yahooapis.com')
    querystring = urllib.urlencode({'q': yql, 'format': 'json', 'env': DATATABLES_URL})
    conn.request('GET', PUBLIC_API_URL + '?' + querystring)
    return json.loads(conn.getresponse().read())

    
class QueryError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
  

def __format_symbol_list(symbol_list):
    return ",".join(["\""+stock+"\"" for stock in symbol_list])
    

def __is_valid_response(response, field):
    return 'query' in response and 'results' in response['query'] \
        and field in response['query']['results']
    

def __validate_response(response, tag_to_check):
    if __is_valid_response(response, tag_to_check):
        quote_info = response['query']['results'][tag_to_check]
    else:
        if 'error' in response:
            raise QueryError('YQL query failed with error: "%s".' 
                % response['error']['description'])
        else:
            raise QueryError('YQL response malformed.')
    return quote_info


def get_current_info(symbol_list, columns_store_retrieve='*'):
    """(15 minute delay)"""
    
    columns = ','.join(columns_store_retrieve)
    symbols = __format_symbol_list(symbol_list)

    yql = 'select %s from %s where symbol in (%s)' \
          %(columns, FINANCE_TABLES['quotes'], symbols)
    response = execute_yql_query(yql)
    return __validate_response(response, 'quote')


def get_historical_info(symbol):
    yql = 'select * from csv where url=\'%s\'' \
          ' and columns=\"Date,Open,High,Low,Close,Volume,AdjClose\"' \
           % (HISTORICAL_URL + symbol)
    results = execute_yql_query(yql)
    # delete first row which contains column names
    del results['query']['results']['row'][0]
    return results['query']['results']['row']
    

def get_news_feed(symbol):
    feed_url = RSS_URL + symbol
    yql = 'select title, link, description, pubDate from rss where url=\'%s\'' % feed_url
    response = execute_yql_query(yql)
    if response['query']['results']['item'][0]['title'].find('not found') > 0:
        raise QueryError('Feed for %s does not exist.' % symbol)
    else:
        return response['query']['results']['item']

    
def get_options_info(symbol, expiration='', columns_store_retrieve='*'):
    columns = ','.join(columns_store_retrieve)
    yql = 'select %s from %s where symbol = \'%s\'' \
          % (columns, FINANCE_TABLES['options'], symbol)
    
    if expiration != '':
        yql += " and expiration='%s'" %(expiration)
    
    response = execute_yql_query(yql)
    return __validate_response(response, 'optionsChain')

    
def get_index_summary(index, columns_store_retrieve='*'):
    columns = ','.join(columns_store_retrieve)
    yql = 'select %s from %s where symbol = \'@%s\'' \
          % (columns, FINANCE_TABLES['quoteslist'], index)
    response = execute_yql_query(yql)
    return __validate_response(response, 'quote')


def get_industry_ids():
    yql = 'select * from %s' % FINANCE_TABLES['sectors']
    response = execute_yql_query(yql)
    return __validate_response(response, 'sector')


def get_industry_index(id):
    yql = 'select * from %s where id =\'%s\'' \
          % (FINANCE_TABLES['industry'], id)
    response = execute_yql_query(yql)
    return __validate_response(response, 'industry')
        

