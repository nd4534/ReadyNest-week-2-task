import pandas as pd

def calculate_weighted_rfm():
    print("Step 1: Ingesting cleaned transactional data...")
    df = pd.read_csv('outputs/cleaned_customer_dataset.csv')
    
    # Fixed the format warning by setting dayfirst=True
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')
    snapshot_date = df['Order Date'].max()
    
    print("Step 2: Calculating core R, F, and M metrics per customer...")
    customer_df = df.groupby('Customer ID').agg({
        'Order Date': lambda x: (snapshot_date - x.max()).days,
        'Order ID': 'nunique',
        'Sales': 'sum'
    }).rename(columns={'Order Date': 'Recency', 'Order ID': 'Frequency', 'Sales': 'Monetary'})
    
    print("Step 3: Scoring metrics into uniform quintiles (1-5)...")
    customer_df['R_Score'] = pd.qcut(customer_df['Recency'].rank(method='first'), 5, labels=[5, 4, 3, 2, 1]).astype(int)
    customer_df['F_Score'] = pd.qcut(customer_df['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    customer_df['M_Score'] = pd.qcut(customer_df['Monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    print("Step 4: Compounding balanced 40/30/30 weighted RFM equations...")
    # Updated ratio: 40% Monetary, 30% Frequency, 30% Recency
    customer_df['Weighted_Score'] = (
        (customer_df['R_Score'] * 0.30) + 
        (customer_df['F_Score'] * 0.30) + 
        (customer_df['M_Score'] * 0.40)
    )
    
    print("Step 5: Allocating optimized customer tier structures...")
    # Reshaped percentiles: Low (0-50%), Medium (50-94%), High (Top 6% of power-buyers)
    customer_df['Customer Segment'] = pd.qcut(
        customer_df['Weighted_Score'].rank(method='first'),
        q=[0, 0.50, 0.94, 1.0],
        labels=['Low Value', 'Medium Value', 'High Value']
    )
    
    segment_lookup = customer_df['Customer Segment'].to_dict()
    df['Customer Segment'] = df['Customer ID'].map(segment_lookup)
    
    df.to_csv('outputs/cleaned_customer_dataset.csv', index=False)
    
    print("\n--- OPTIMIZED WEIGHTED TRANSACTION DISTRIBUTION ---")
    print(df['Customer Segment'].value_counts())
    print("\nSUCCESS: Optimized Weighted RFM processing completed!")

if __name__ == '__main__':
    calculate_weighted_rfm()