import pandas as pd
import matplotlib.pyplot as plt

file_path = "/Users/sg/Desktop/courses/winter-2025/4nl3/4NL3-group-project/phase-3/ground_truth_complete.csv" 

df = pd.read_csv(file_path)

true_columns = ['True Pos', 'True Neg', 'True Team', 'True Individual']
df_true = df[true_columns]

class_distribution = df_true.sum()

plt.figure(figsize=(14, 10))
class_distribution.plot(kind='bar', color=['blue', 'red', 'green', 'purple'])
plt.title("Class Distribution Analysis")
plt.xlabel("Categories")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('class_distribution_plot.png')