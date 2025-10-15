import random
import numpy as np
import matplotlib.pyplot as plt

random.seed(42)
np.random.seed(42)

random_integer = random.randint(1, 20)
print(f"Random integer: {random_integer}")

random_float = random.uniform(0.5, 5.0)
print(f"Random float: {random_float:.3f}")

normal_numbers = np.random.normal(loc=2.0, scale=0.8, size=1000)

plt.hist(normal_numbers, bins=25, color='skyblue', edgecolor='navy', alpha=0.7)
plt.axvline(np.mean(normal_numbers), color='red', linestyle='dashed', linewidth=1.5, label='Mean')

plt.title("Modified Normal Distribution Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.legend()
plt.grid(alpha=0.3)
plt.show()