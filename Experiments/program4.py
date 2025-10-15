from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd

mall_df = pd.read_csv("/Mall_Customers.csv")
print("Mall Customers dataset loaded successfully.")
print(mall_df.head())

X = mall_df[['Annual Income (k$)', 'Spending Score (1-100)']].values

kmeans = KMeans(n_clusters=5, random_state=0, n_init=10)
kmeans.fit(X)
y_kmeans = kmeans.predict(X)

plt.figure(figsize=(10, 7))
plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.75, marker='X')
plt.title("K-Means Clustering of Mall Customers")
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score (1-100)")
plt.show()