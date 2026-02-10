import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
df = pd.read_csv('kaggle_salaries_data.csv')
salaries = df['salary_in_usd'].values

print(f"Salary range: ${salaries.min():,.0f} - ${salaries.max():,.0f}")
print(f"Total data points: {len(salaries)}")
print(f"Mean: ${salaries.mean():,.0f}")
print(f"Median: ${np.median(salaries):,.0f}")
print(f"Std Dev: ${salaries.std():,.0f}")
print(f"Skewness: {pd.Series(salaries).skew():.3f}")

# Create histogram
fig, ax = plt.subplots(figsize=(12, 6), facecolor='#000000')
ax.set_facecolor('#000000')

ax.hist(salaries, bins=30, edgecolor='white', linewidth=1.5, color='#C3C3C3', zorder=3)
ax.set_xlabel('Salary (USD)', fontsize=16, color='white', weight='bold')
ax.set_ylabel('Number of Occurrences', fontsize=16, color='white', weight='bold')
ax.set_ylim(0, 3000)
ax.grid(axis='y', color='white', zorder=0)
ax.tick_params(colors='white', labelsize=14)
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['bottom'].set_linewidth(2.5)
ax.spines['left'].set_linewidth(2.5)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.tight_layout()

# Save and show
plt.savefig('media/images/salary_histogram.png', dpi=150, bbox_inches='tight')
plt.show()
