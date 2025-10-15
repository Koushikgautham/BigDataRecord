import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

transactions = [['milk', 'bread', 'eggs'],
                ['bread', 'jam'],
                ['milk', 'bread', 'jam', 'cereal'],
                ['milk', 'sugar'],
                ['bread', 'sugar']]

te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df = pd.DataFrame(te_ary, columns=te.columns_)

frequent_itemsets = apriori(df, min_support=0.4, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
print("--- Frequent Itemsets ---")
print(frequent_itemsets)
print("\n--- Association Rules ---")
print(rules[['antecedents', 'consequents', 'support', 'confidence']])