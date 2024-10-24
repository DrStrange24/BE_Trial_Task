from django.core.management.base import BaseCommand
import requests
from finance.models import StockData
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch stock data from Alpha Vantage'

    def handle(self, *args, **kwargs):
        API_KEY = '57IAIXJKIBN6D7AG'
        SYMBOL = 'AAPL'
        URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}'

        response = requests.get(URL)
        data = response.json()

        if "Time Series (Daily)" in data:
            time_series = data["Time Series (Daily)"]
            for date_str, daily_data in time_series.items():
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                StockData.objects.update_or_create(
                    symbol=SYMBOL,
                    date=date,
                    defaults={
                        'open_price': daily_data['1. open'],
                        'high_price': daily_data['2. high'],
                        'low_price': daily_data['3. low'],
                        'close_price': daily_data['4. close'],
                        'volume': daily_data['5. volume'],
                    }
                )
            self.stdout.write('Success')
        else:
            self.stdout.write('Failed to fetch data. Check your API limits or API key.')
