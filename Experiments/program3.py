import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
try:
    housing_df = pd.read_csv("/Housing.csv")
    print("Housing dataset loaded successfully.")
    display(housing_df.head())
    
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=housing_df, x="area", y="price", hue="furnishingstatus")
    plt.title("Price vs. Area of Houses")
    plt.xlabel("Area")
    plt.ylabel("Price")
    plt.show()
    
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=housing_df, x="bedrooms", y="price")
    plt.title("Distribution of House Prices by Number of Bedrooms")
    plt.xlabel("Number of Bedrooms")
    plt.ylabel("Price")
    plt.show()

except FileNotFoundError:
    print("Error: The file '/Housing.csv' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")