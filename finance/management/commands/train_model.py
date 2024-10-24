from django.core.management.base import BaseCommand
from finance.models import StockData
from sklearn.linear_model import LinearRegression
import numpy as np
import pickle
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Train a linear regression model using historical stock data and save as model.pkl'

    def handle(self, *args, **kwargs):
        # Fetch historical data from the database
        data = StockData.objects.all().order_by('date')
        if not data.exists():
            self.stdout.write(self.style.ERROR('No historical data found in the database.'))
            return

        # Prepare data for training (e.g., using closing prices)
        dates = np.array([(entry.date - data[0].date).days for entry in data]).reshape(-1, 1)
        closing_prices = np.array([entry.close_price for entry in data]).reshape(-1, 1)

        # Train a linear regression model
        model = LinearRegression()
        model.fit(dates, closing_prices)

        # Save the trained model to a .pkl file
        model_path = os.path.join(settings.BASE_DIR, 'finance/model.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

        self.stdout.write(self.style.SUCCESS(f'Model trained and saved as {model_path}'))
