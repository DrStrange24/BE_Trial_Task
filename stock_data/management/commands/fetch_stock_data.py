import requests
from django.core.management.base import BaseCommand
from stock_data.models import StockData
from django.conf import settings

class Command(BaseCommand):
    help = 'Fetch daily stock data from Alpha Vantage'

    def handle(self, *args, **kwargs):
        symbol = 'AAPL'
        api_key = settings.ALPHA_VANTAGE_API_KEY
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print('log: ',data)
            time_series = data.get('Time Series (Daily)', {})
            for date, daily_data in time_series.items():
                print(f"Date: {date}, Data: {daily_data}")
                StockData.objects.update_or_create(
                    stock_symbol=symbol,
                    date=date,
                    defaults={
                        'open_price': daily_data['1. open'],
                        'high_price': daily_data['2. high'],
                        'low_price': daily_data['3. low'],
                        'close_price': daily_data['4. close'],
                        'volume': daily_data['6. volume']
                    }
                )
            self.stdout.write(self.style.SUCCESS('Successfully fetched and stored data.'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch data.'))
