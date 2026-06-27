import pandas as pd
import numpy as np

# 1. Load the original raw, uncleaned dataset
# Replace with the exact path to your raw uncleaned source file
raw_df = pd.read_csv('dataset/Global_Superstore2.csv', encoding='latin1') 

# 2. Create a clean expansion matrix (approx 55k rows to push total over 1 Lakh)
expansion_df = raw_df.copy()

# 3. Inject brand new growth countries and target regions to maximize the map
new_countries = [
    'Kenya', 'Egypt', 'Nigeria', 'South Africa', 'Senegal', 'Ghana', # African Hubs
    'Netherlands', 'Spain', 'Italy', 'Argentina', 'Indonesia', 'Japan' # Expanded Global Hubs
]

# Randomly assign these new countries across the expansion rows
expansion_df['Country'] = np.random.choice(new_countries, size=len(expansion_df))

# Map markets to match the newly injected countries dynamically
market_mapping = {
    'Kenya': 'Africa', 'Egypt': 'Africa', 'Nigeria': 'Africa', 'South Africa': 'Africa', 
    'Senegal': 'Africa', 'Ghana': 'Africa', 'Netherlands': 'EU', 'Spain': 'EU', 
    'Italy': 'EU', 'Argentina': 'LATAM', 'Indonesia': 'APAC', 'Japan': 'APAC'
}
expansion_df['Market'] = expansion_df['Country'].map(market_mapping)

# 4. Advance order dates to 2015-2018 to simulate forward timeline growth
if 'Order Date' in expansion_df.columns:
    date_str = expansion_df['Order Date'].astype(str)
    expansion_df['Order Date'] = date_str.str.replace('2011', '2015').str.replace('2012', '2016').str.replace('2013', '2017').str.replace('2014', '2018')

# 5. Generate unique Row IDs and modify transaction values with random noise
if 'Row ID' in expansion_df.columns:
    expansion_df['Row ID'] = expansion_df['Row ID'] + raw_df['Row ID'].max()

if 'Sales' in expansion_df.columns:
    expansion_df['Sales'] = (expansion_df['Sales'] * np.random.uniform(0.90, 1.15, size=len(expansion_df))).round(2)

if 'Profit' in expansion_df.columns:
    expansion_df['Profit'] = (expansion_df['Profit'] * np.random.uniform(0.90, 1.15, size=len(expansion_df))).round(2)

# 6. Merge the original uncleaned rows with our engineered growth data
uncleaned_lakh_dataset = pd.concat([raw_df, expansion_df], ignore_index=True)

# 7. Save out to your raw directory file to clean down the line
uncleaned_lakh_dataset.to_csv('dataset/uncleaned_lakh_dataset.csv', index=False)

print("SUCCESS: Raw uncleaned pipeline generated successfully!")
print(f"Total Rows: {len(uncleaned_lakh_dataset)} | New Countries Injected: {len(new_countries)}")