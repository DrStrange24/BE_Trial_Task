from django.http import JsonResponse
from .backtesting import run_backtest

#http://127.0.0.1:8000/finance/backtest/?symbol=AAPL&initial_investment=10000&short_window=5&long_window=20
def backtest_view(request):
    symbol = request.GET.get('symbol', 'AAPL')
    initial_investment = float(request.GET.get('initial_investment', 10000))
    short_window = int(request.GET.get('short_window', 50))
    long_window = int(request.GET.get('long_window', 200))

    result = run_backtest(symbol, initial_investment, short_window, long_window)
    return JsonResponse(result)
