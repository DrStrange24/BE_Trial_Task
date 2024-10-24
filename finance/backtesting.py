from finance.models import StockData
from django.db.models import Avg

def run_backtest(symbol, initial_investment, short_window=50, long_window=200):
    data = StockData.objects.filter(symbol=symbol).order_by('date')
    cash = initial_investment
    stock = 0
    trades = 0
    max_drawdown = 0
    peak = initial_investment

    # Convert QuerySet to list to avoid querying again in each loop iteration
    data_list = list(data)

    for idx, entry in enumerate(data):
        # print(idx,entry.symbol,entry.date)
        if idx >= long_window:  # Make sure we have enough data to calculate moving averages
            short_ma = StockData.objects.filter(
                symbol=symbol,
                date__lte=entry.date
            ).order_by('-date')[:short_window].aggregate(Avg('close_price'))['close_price__avg']

            long_ma = StockData.objects.filter(
                symbol=symbol,
                date__lte=entry.date
            ).order_by('-date')[:long_window].aggregate(Avg('close_price'))['close_price__avg']

            if short_ma and long_ma:
                if entry.close_price < short_ma and cash > entry.close_price:
                    # Buy
                    stock += cash // float(entry.close_price)
                    cash %= float(entry.close_price)
                    trades += 1
                elif entry.close_price > long_ma and stock > 0:
                    # Sell
                    cash += stock * float(entry.close_price)
                    stock = 0
                    trades += 1

            # Update peak and drawdown
            current_value = cash + (stock * float(entry.close_price) if stock > 0 else 0)
            if current_value > peak:
                peak = current_value
            drawdown = (peak - current_value) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown

    total_value = cash + (stock * float(data_list[-1].close_price) if stock > 0 else 0)
    return {
        'total_value': total_value,
        'cash': cash,
        'stock': stock,
        'trades': trades,
        'max_drawdown': max_drawdown
    }
