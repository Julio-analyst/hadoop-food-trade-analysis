import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('dataset.csv')


print(df.head())

display_cols = ['reporterDesc', 'refYear', 'cmdDesc', 'total_cifvalue', 'total_quantity']
print(df[display_cols].head())

plt.figure(figsize=(12, 6))
sns.barplot(
    data=df,
    x='refYear',
    y='total_cifvalue',
    hue='cmdDesc',
    ci=None
)
plt.title('Total CIF Value by Year and Commodity')
plt.xlabel('Year')
plt.ylabel('Total CIF Value')
plt.legend(title='Commodity')
plt.tight_layout()
plt.show()

print(df.columns)  