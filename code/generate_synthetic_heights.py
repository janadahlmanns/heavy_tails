import pandas as pd
import numpy as np

# Generate 100 measurements with mean 172, sd 10
np.random.seed(42)
heights = np.random.normal(loc=172, scale=10, size=100)
heights = np.round(heights).astype(int)

# Create dataframe
df = pd.DataFrame({'Height': heights})

# Save to new file
df.to_csv('height_synthetic.csv', index=False)

print(f"Generated {len(heights)} synthetic measurements")
print(f"Mean: {heights.mean():.2f} cm")
print(f"Std Dev: {heights.std():.2f} cm")
print(f"Range: {heights.min()}-{heights.max()} cm")
print(f"\nSaved to height_synthetic.csv")
