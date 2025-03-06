import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("account_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://finance-department-3f0ba-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# Function to fetch sales data
def fetch_sales_data():
    ref = db.reference("sales")  # Adjust the collection name if needed
    sales_data = ref.get()
    
    records = []
    for key, value in sales_data.items():
        if "earnings" in value and "timestamp" in value:
            records.append({
                "date": datetime.strptime(value["timestamp"], "%Y-%m-%d %H:%M:%S"),
                "earnings": float(value["earnings"])
            })
    
    df = pd.DataFrame(records).sort_values(by="date")
    df.set_index("date", inplace=True)
    
    # Resample to ensure consistent monthly data (fill missing months with 0 earnings)
    df = df.resample("M").sum().fillna(0)
    
    return df

# Train and forecast using ARIMA
def forecast_sales(df, periods=12):  # Forecast for next 12 months
    # Fit ARIMA model (Auto ARIMA can also be used)
    model = sm.tsa.ARIMA(df["earnings"], order=(1, 1, 1))  # Adjust order as needed
    model_fit = model.fit()

    # Forecast for the next 12 months
    forecast = model_fit.forecast(steps=periods)
    future_dates = pd.date_range(start=df.index[-1], periods=periods+1, freq="M")[1:]

    # Plot results
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["earnings"], label="Historical Earnings", marker="o", linestyle="solid")
    plt.plot(future_dates, forecast, label="Forecasted Earnings", marker="o", linestyle="dashed", color="red")
    plt.xlabel("Date")
    plt.ylabel("Earnings")
    plt.title("Sales Earnings Forecast (Next 12 Months)")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Print forecast values
    forecast_df = pd.DataFrame({"Date": future_dates, "Forecasted Earnings": forecast})
    print(forecast_df)

# Main execution
if __name__ == "__main__":
    sales_df = fetch_sales_data()
    print(sales_df)  # Print fetched data for reference
    if not sales_df.empty:
        forecast_sales(sales_df)
    else:
        print("No sales data found!")
