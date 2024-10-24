from django.test import TestCase
from .backtesting import run_backtest
from .models import StockData
from datetime import date

class BacktestingTestCase(TestCase):
    def setUp(self):
        # Set up initial data for testing
        StockData.objects.create(symbol='AAPL', date=date(2023, 1, 1), open_price=100, high_price=110, low_price=90, close_price=105, volume=1000)
        StockData.objects.create(symbol='AAPL', date=date(2023, 1, 2), open_price=106, high_price=112, low_price=102, close_price=108, volume=1200)
        StockData.objects.create(symbol='AAPL', date=date(2023, 1, 3), open_price=107, high_price=115, low_price=105, close_price=110, volume=1500)

    def test_run_backtest(self):
        # Run backtest with initial parameters
        result = run_backtest('AAPL', 10000)
        self.assertIsNotNone(result)
        self.assertIn('total_value', result)
        self.assertIn('trades', result)
