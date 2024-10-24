import pandas as pd
from stock_data.models import StockData

def simple_moving_average_strategy(stock_symbol, initial_investment, short_window=50, long_window=200):
    # Fetch historical data from the database
    stock_records = StockData.objects.filter(stock_symbol=stock_symbol).order_by('date')
    if not stock_records.exists():
        return {"error": "No data found for this stock symbol."}

    # Convert to pandas DataFrame
    data = pd.DataFrame.from_records(stock_records.values())
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)

    # Calculate moving averages
    data['short_mavg'] = data['close_price'].rolling(window=short_window).mean()
    data['long_mavg'] = data['close_price'].rolling(window=long_window).mean()

    # Initialize positions and cash
    position = 0
    cash = initial_investment
    for date, row in data.iterrows():
        if row['short_mavg'] is not None and row['long_mavg'] is not None:
            if row['short_mavg'] > row['long_mavg'] and position == 0:
                # Buy signal
                position = cash / row['close_price']
                cash = 0
            elif row['short_mavg'] < row['long_mavg'] and position > 0:
                # Sell signal
                cash = position * row['close_price']
                position = 0

    # Calculate final portfolio value
    portfolio_value = cash + (position * data['close_price'].iloc[-1] if position > 0 else 0)

    # Calculate performance metrics
    return_on_investment = ((portfolio_value - initial_investment) / initial_investment) * 100
    total_trades = len(data.dropna(subset=['short_mavg', 'long_mavg']))

    # Return the backtesting results
    return {
        "final_portfolio_value": portfolio_value,
        "return_on_investment": return_on_investment,
        "total_trades": total_trades
    }
