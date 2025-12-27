from datetime import datetime, timedelta
import sqlite3

class Forecaster:
    def __init__(self, db_path="kasir.db"):
        self.db_path = db_path

    def get_forecast(self, days_to_predict=7):
        # 1. Get historical data (last 30 days)
        data = self._get_daily_sales_history(limit=30)
        if len(data) < 2:
            return None # Not enough data

        # 2. Prepare X (day index) and Y (revenue)
        # Sort by date
        data.sort(key=lambda x: x['date'])
        
        X = list(range(len(data)))
        Y = [d['total'] for d in data]

        # 3. Linear Regression (y = mx + b)
        n = len(X)
        sum_x = sum(X)
        sum_y = sum(Y)
        sum_xy = sum(x*y for x,y in zip(X,Y))
        sum_xx = sum(x*x for x in X)

        # Calculate slope (m) and intercept (b)
        try:
            m = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
            b = (sum_y - m * sum_x) / n
        except ZeroDivisionError:
            m = 0
            b = sum_y / n

        # 4. Predict Future
        last_date_obj = datetime.strptime(data[-1]['date'], "%Y-%m-%d")
        predictions = []
        
        current_x = X[-1]
        for i in range(1, days_to_predict + 1):
            next_x = current_x + i
            pred_y = m * next_x + b
            pred_y = max(0, pred_y) # No negative sales
            
            next_date = last_date_obj + timedelta(days=i)
            predictions.append({
                'date': next_date.strftime("%Y-%m-%d"),
                'predicted_total': pred_y
            })
            
        return {
            'historical': data,
            'forecast': predictions,
            'trend': 'UP' if m > 0 else 'DOWN'
        }

    def _get_daily_sales_history(self, limit=30):
        # Simple query
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get dates and sums
        end_date = datetime.now()
        start_date = end_date - timedelta(days=limit)
        
        start_str = start_date.strftime("%Y-%m-%d")
        
        # Group by date
        # Note: 'date' column in transactions is TIMESTAMP 'YYYY-MM-DD HH:MM:SS' usually, need to slice
        cursor.execute('''
            SELECT substr(date, 1, 10) as day, SUM(final_total) 
            FROM transactions 
            WHERE status = 'SUCCESS' AND date >= ? 
            GROUP BY day
        ''', (start_str,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{'date': r[0], 'total': r[1]} for r in rows]
