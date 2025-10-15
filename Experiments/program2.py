import pandas as pd
import numpy as np
from scipy import stats

try:
    your_dataset_path = "/Housing.csv"
    your_df = pd.read_csv(your_dataset_path)
    
    print(f"Dataset loaded successfully from {your_dataset_path}")
    display(your_df.head())
    
    print("\nPopulation Distribution Analysis for your Dataset:")
    for col in your_df.select_dtypes(include=np.number).columns:
        mean_value = np.mean(your_df[col])
        median_value = np.median(your_df[col])
        if not your_df[col].empty:
            mode_result = stats.mode(your_df[col])
        else:
            mode_result = None
            print(f"\nFeature: {col}")
            print(f"  Mean: {mean_value:.3f}")
            print(f"  Median: {median_value:.3f}")
            if mode_result:
                if isinstance(mode_result.mode, np.ndarray):
                    print(f"  Mode: {mode_result.mode} (count: {mode_result.count})")
                else:
                    print(f"  Mode: {mode_result.mode:.3f} (count: {mode_result.count})")
            else:
                print("  Mode: Could not calculate mode for empty data.")

except FileNotFoundError:
    print(f"Error: The file '{your_dataset_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")