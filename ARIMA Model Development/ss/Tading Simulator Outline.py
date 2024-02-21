import pandas as pd
import numpy as np

class TradingSimulator:
    def __init__(self, initial_cash=100000):
        self.cash = initial_cash
        self.assets = 0
        self.transaction_cost = 0.001  # 0.1% per trade
        self.data = None
        self.signal = None
        self.trades = []
    
    def load_data(self, data):
        self.data = data
    
    def generate_signal(self, model):
        # Placeholder for signal generation logic using ARIMA model
        self.signal = model.predict()
    
    def execute_trade(self, timestamp, price, signal):
        if signal > 0 and self.cash >= price:
            # Buy one unit
            self.assets += 1
            self.cash -= price * (1 + self.transaction_cost)
            self.trades.append((timestamp, price, 'BUY'))
        elif signal < 0 and self.assets > 0:
            # Sell one unit
            self.assets -= 1
            self.cash += price * (1 - self.transaction_cost)
            self.trades.append((timestamp, price, 'SELL'))
    
    def simulate(self):
        for index, row in self.data.iterrows():
            self.generate_signal(model)  # You'd pass your ARIMA model here
            self.execute_trade(row['timestamp'], row['mid_price'], self.signal)
    
    def calculate_performance(self):
        # Placeholder for performance calculation logic
        pass

# Usage:
simulator = TradingSimulator(initial_cash=100000)
historical_data = pd.DataFrame({
    'timestamp': pd.date_range(start='2020-01-01', periods=100, freq='T'),
    'mid_price': np.random.normal(100, 0.5, 100)  # Randomly generated prices
})
simulator.load_data(historical_data)
simulator.simulate()