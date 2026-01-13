import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the filtered data
df = pd.read_csv('height_filtered.csv')
heights = df['Height'].values

print(f"Filtered male heights (>150cm): {heights.min():.2f} - {heights.max():.2f} cm")
print(f"Total data points: {len(heights)}")
print(f"Mean: {heights.mean():.2f} cm")
print(f"Std Dev: {heights.std():.2f} cm")
print(f"Skewness: {pd.Series(heights).skew():.3f}")

# Create bins for all three widths
min_height = np.floor(heights.min() - 0.5)
max_height = np.ceil(heights.max() + 0.5)

bins_1cm = np.arange(min_height, max_height + 1, 1)
bins_2cm = np.arange(min_height, max_height + 1, 2)
bins_5cm = np.arange(min_height, max_height + 1, 5)

# Plot side by side with different bin widths
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# 1cm bin width
axes[0].hist(heights, bins=bins_1cm, edgecolor='black', alpha=0.7, color='#AFCBCF')
axes[0].set_xlabel('Height (cm)', fontsize=12)
axes[0].set_ylabel('Number of Occurrences', fontsize=12)
axes[0].set_title('Bin Width: 1 cm', fontsize=14)
axes[0].grid(axis='y', alpha=0.3)

# 2cm bin width
axes[1].hist(heights, bins=bins_2cm, edgecolor='black', alpha=0.7, color='#AFCBCF')
axes[1].set_xlabel('Height (cm)', fontsize=12)
axes[1].set_ylabel('Number of Occurrences', fontsize=12)
axes[1].set_title('Bin Width: 2 cm', fontsize=14)
axes[1].grid(axis='y', alpha=0.3)

# 5cm bin width
axes[2].hist(heights, bins=bins_5cm, edgecolor='black', alpha=0.7, color='#AFCBCF')
axes[2].set_xlabel('Height (cm)', fontsize=12)
axes[2].set_ylabel('Number of Occurrences', fontsize=12)
axes[2].set_title('Bin Width: 5 cm', fontsize=14)
axes[2].grid(axis='y', alpha=0.3)

plt.tight_layout()

# Save and show
plt.savefig('media/images/height_histogram.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"\nHistogram saved to media/images/height_histogram.png")
