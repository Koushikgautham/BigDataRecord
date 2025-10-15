import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

try:
    house_df = pd.read_csv("/House Price Prediction Dataset.csv")
    print("House Price Prediction dataset loaded successfully.")
    display(house_df.head())
    
    X = house_df[['Area']].values
    y = house_df['Price'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    lin_reg = LinearRegression()
    lin_reg.fit(X_train, y_train)
    y_pred = lin_reg.predict(X_test)
    plt.figure(figsize=(8, 6))
    plt.scatter(X_test, y_test, color='blue', label='Actual Prices')
    plt.plot(X_test, y_pred, color='red', linewidth=2, label='Predicted Prices')
    plt.title('Linear Regression - House Price Prediction')
    plt.xlabel('Area')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
    
    from sklearn.metrics import mean_squared_error
    mse = mean_squared_error(y_test, y_pred)
    print(f"\nMean Squared Error: {mse:.2f}")

except:
    pass