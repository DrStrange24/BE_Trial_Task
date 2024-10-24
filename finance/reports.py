import matplotlib.pyplot as plt
import io
import base64
from django.http import HttpResponse
from .models import StockData, StockPrediction
from xhtml2pdf import pisa

def generate_report(symbol):
    # Fetch historical and predicted data
    historical_data = StockData.objects.filter(symbol=symbol).order_by('date')
    predicted_data = StockPrediction.objects.filter(symbol=symbol).order_by('date')

    # Generate plot
    dates = [entry.date for entry in historical_data]
    actual_prices = [entry.close_price for entry in historical_data]
    predicted_prices = [entry.predicted_price for entry in predicted_data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, actual_prices, label='Actual Prices', color='blue')
    plt.plot(dates[-len(predicted_prices):], predicted_prices, label='Predicted Prices', color='red')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'Stock Price Prediction for {symbol}')
    plt.legend()

    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return plot_base64

def generate_pdf_report(symbol):
    # Generate the report as HTML
    report_html = f"""
    <html>
    <body>
        <h1>Stock Price Prediction Report for {symbol}</h1>
        <img src="data:image/png;base64,{generate_report(symbol)}" />
    </body>
    </html>
    """

    # Convert HTML to PDF
    result = io.BytesIO()
    pisa.CreatePDF(io.StringIO(report_html), dest=result)
    result.seek(0)
    return result
