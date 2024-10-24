from .backtesting import run_backtest
import pickle
from django.conf import settings
import os
from django.http import JsonResponse
from .models import StockData, StockPrediction
import numpy as np
from datetime import timedelta, date
from django.http import JsonResponse, FileResponse
from .reports import generate_report, generate_pdf_report

#http://127.0.0.1:8000/finance/backtest/?symbol=AAPL&initial_investment=10000&short_window=5&long_window=20
def backtest_view(request):
    symbol = request.GET.get('symbol', 'AAPL')
    initial_investment = float(request.GET.get('initial_investment', 10000))
    short_window = int(request.GET.get('short_window', 50))
    long_window = int(request.GET.get('long_window', 200))

    result = run_backtest(symbol, initial_investment, short_window, long_window)
    return JsonResponse(result)

#http://127.0.0.1:8000/finance/predict/?symbol=AAPL
def predict_view(request):
    symbol = request.GET.get('symbol', 'AAPL')
    if not symbol:
        return JsonResponse({'error': 'Stock symbol is required.'})

    model_path = os.path.join(settings.BASE_DIR, 'finance/model.pkl')

    # Load the pre-trained model
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # Fetch historical data to make predictions
    data = StockData.objects.filter(symbol=symbol).order_by('date')
    if not data.exists():
        return JsonResponse({'error': 'No historical data found for the given symbol.'})

    # Prepare the data for prediction (e.g., using closing prices)
    dates = np.array([(entry.date - data[0].date).days for entry in data]).reshape(-1, 1)

    # Make predictions for the next 30 days
    future_dates = np.array([dates[-1][0] + i for i in range(1, 31)]).reshape(-1, 1)
    predictions = model.predict(future_dates)
    predictions = predictions.flatten().tolist()

    # Store predictions in the database
    prediction_date = data.last().date
    for i, predicted_price in enumerate(predictions):
        prediction_date += timedelta(days=1)
        StockPrediction.objects.update_or_create(
            symbol=symbol,
            date=prediction_date,
            defaults={'predicted_price': predicted_price}
        )

    # Return predictions
    return JsonResponse({'symbol': symbol, 'predictions': predictions})

# http://127.0.0.1:8000/finance/report/?symbol=AAPL&format=json
# http://127.0.0.1:8000/finance/report/?symbol=AAPL&format=pdf
def report_view(request):
    symbol = request.GET.get('symbol', 'AAPL')
    format = request.GET.get('format', 'json')

    if format == 'pdf':
        pdf = generate_pdf_report(symbol)
        return FileResponse(pdf, as_attachment=True, filename=f'{symbol}_report.pdf')
    else:
        plot_base64 = generate_report(symbol)
        return JsonResponse({'symbol': symbol, 'plot': plot_base64})
