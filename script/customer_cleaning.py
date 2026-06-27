import pandas as pd

def clean_raw_data():
    print("Step 1: Reading raw uncleaned lakh dataset...")
    df = pd.read_csv('dataset/uncleaned_lakh_dataset.csv', encoding='latin1')
    initial_rows = len(df)
    
    # Trim column headers
    # Trim column headers
    df.columns = [col.strip() for col in df.columns] if hasattr(df.columns, 'str') else [col.strip() for col in df.columns]
    
    print("Step 2: Dropping useless Postal Code column...")
    # Drop the column safely if it exists in the dataset
    if 'Postal Code' in df.columns:
        df.drop(columns=['Postal Code'], inplace=True)
    
    print("Step 3: Dropping rows missing critical customer identifiers...")
    df.dropna(subset=['Row ID', 'Customer ID', 'Sales', 'Profit'], inplace=True)
    
    print("Step 4: Standardizing IDs and Casing...")
    df['Customer ID'] = df['Customer ID'].astype(str).str.strip().str.upper()
    df['Customer Name'] = df['Customer Name'].astype(str).str.strip()
    if 'Market' in df.columns:
        df['Market'] = df['Market'].astype(str).str.strip().str.upper()

    print("Step 5: Ensuring realistic financial values...")
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0).abs()
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce').fillna(0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(1).abs()
    
    # Save the lean, clean dataset
    df.to_csv('outputs/cleaned_customer_dataset.csv', index=False)
    print(f"SUCCESS: Dropped 'Postal Code' and saved {len(df)} pristine rows!")

if __name__ == '__main__':
    clean_raw_data()