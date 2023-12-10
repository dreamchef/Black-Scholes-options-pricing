import json
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

EODMETRICS_API_KEY = os.environ.get('EODMETRICS_API_KEY')
API_BASE_URL = 'https://api.eodmetrics.com/query'
API_PARAMS = urllib.parse.urlencode({
    'apiKey': EODMETRICS_API_KEY,
    'format': 'json',
    'data': json.dumps({
        'fields': ['ticker'],
        'conditions': [
            {'field': 'close_price', 'operator': 'gt', 'value': '5.00'},
            {'field': 'volume', 'operator': 'gt', 'value': '100000'}
        ],
        'tickers': [],
        'order': [{'field': 'market_cap', 'direction': 'desc'}]
    })
})
N_TICKERS = 200