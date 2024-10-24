from django.core.management.base import BaseCommand
import requests
from finance.models import StockData
from datetime import datetime, timedelta
import time
import os

class Command(BaseCommand):
    help = 'Fetch stock data from Alpha Vantage'

    def handle(self, *args, **kwargs):
        API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
        SYMBOL = 'AAPL'
        URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}'
        MAX_RETRIES = 5
        RETRY_DELAY = 60  # 60 seconds

        retries = 0
        while retries < MAX_RETRIES:
            try:
                response = requests.get(URL)
                response.raise_for_status()
                data = response.json()

                if "Note" in data:
                    self.stdout.write(self.style.WARNING('Rate limit reached. Retrying after delay...'))
                    time.sleep(RETRY_DELAY)
                    retries += 1
                    continue

                if "Time Series (Daily)" in data:
                    time_series = data["Time Series (Daily)"]
                    two_years_ago = datetime.now().date() - timedelta(days=730)

                    for date_str, daily_data in time_series.items():
                        date = datetime.strptime(date_str, '%Y-%m-%d').date()
                        if date >= two_years_ago:
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
                    self.stdout.write(self.style.SUCCESS('Successfully fetched and stored data.'))
                    break
                else:
                    self.stdout.write(self.style.ERROR('Failed to fetch data. Check your API limits or API key.'))
                    break
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Network error: {e}. Retrying...'))
                retries += 1
                time.sleep(RETRY_DELAY)
        else:
            self.stdout.write(self.style.ERROR('Max retries reached. Failed to fetch data.'))
