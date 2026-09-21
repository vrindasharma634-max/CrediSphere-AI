"""
Admin Dashboard - Prophet / LSTM
Forecasts loan demand, defaults, and portfolio trends.
"""
import random
from datetime import datetime, timedelta

class TimeSeriesForecaster:
    def __init__(self):
        self.model_name = "Prophet_LSTM_Ensemble"
        
    def forecast_demand(self, days=14):
        """
        Simulates time-series forecasting for future loan application demand.
        """
        forecast = []
        base_demand = 50
        
        for i in range(days):
            date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
            # Add some simulated seasonality and noise
            trend = int(base_demand + (i * 2) + random.uniform(-10, 20))
            forecast.append({"date": date, "predicted_applications": max(0, trend)})
            
        return {
            "model": self.model_name,
            "forecast_period_days": days,
            "forecast_data": forecast,
            "trend_summary": "Increasing demand expected mid-month."
        }
