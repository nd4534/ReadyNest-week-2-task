import pandas as pd
import matplotlib.pyplot as plt

def export_all_charts_simple():
    print("Ingesting master dataset using standard graphics pipeline...")
    df = pd.read_csv('outputs/cleaned_customer_dataset.csv')
    
    # Set a clean native Matplotlib style profile
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['figure.figsize'] = (10, 6)
    
    # ----------------------------------------------------
    # CHART 1: Customer Segment Distribution (Pie Chart)
    # ----------------------------------------------------
    print("Generating Chart 1: Customer Segment Distribution...")
    segment_counts = df.groupby('Customer Segment')['Customer ID'].nunique()
    
    plt.figure(figsize=(8, 8))
    colors = ['#0a192f', '#e65c00', '#0099ff']
    
    plt.pie(
        segment_counts, 
        labels=segment_counts.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=colors,
        textprops={'fontsize': 12, 'weight': 'bold'}
    )
    plt.title('Customer Segment Volume & Distribution (Unique Count)', fontsize=14, weight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('outputs/charts/customer_segment_distribution.png', dpi=300)
    plt.close()

    # ----------------------------------------------------
    # CHART 2: Revenue vs Profitability by Category (Combo Chart)
    # ----------------------------------------------------
    print("Generating Chart 2: Category Financial Performance...")
    cat_data = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Primary axis: Sales Bar Chart using standard plt.bar
    ax1.bar(cat_data['Category'], cat_data['Sales'], color='#0d6efd', alpha=0.85, width=0.6)
    ax1.set_title('Revenue Performance vs. Profitability by Category', fontsize=14, weight='bold', pad=15)
    ax1.set_ylabel('Total Sales Revenue ($)', fontsize=12, weight='bold')
    ax1.set_xlabel('Product Category', fontsize=12, weight='bold')
    ax1.grid(True, axis='y', linestyle='--', alpha=0.7) # Native subtle grid lines
    
    # Secondary axis: Profit Line Chart
    ax2 = ax1.twinx()
    ax2.plot(cat_data['Category'], cat_data['Profit'], color='#0a192f', marker='o', linewidth=3, markersize=8)
    ax2.set_ylabel('Net Profit ($)', fontsize=12, weight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/charts/category_financial_performance.png', dpi=300)
    plt.close()

    # ----------------------------------------------------
    # CHART 3: Fulfillment Operational Matrix (Scatter / Bubble Plot)
    # ----------------------------------------------------
    print("Generating Chart 3: Fulfillment Operational Matrix...")
    priority_data = df.groupby('Order Priority').agg({'Quantity': 'sum', 'Profit': 'sum', 'Sales': 'sum'}).reset_index()
    
    plt.figure(figsize=(10, 6))
    
    # Scale bubble sizes manually without Seaborn's assistance
    base_sizes = (priority_data['Sales'] / priority_data['Sales'].max()) * 800 + 200
    
    # Color mapping dictionary for priority categories
    color_map = {'Critical': '#d62728', 'High': '#1f77b4', 'Medium': '#9467bd', 'Low': '#ff7f0e'}
    point_colors = priority_data['Order Priority'].map(color_map)
    
    # Generate scatter plot using native plt.scatter
    scatter = plt.scatter(
        priority_data['Quantity'], 
        priority_data['Profit'], 
        s=base_sizes,
        c=point_colors,
        alpha=0.9,
        edgecolors='black',
        linewidth=1
    )
    
    plt.title('Fulfillment Matrix: Order Volume vs. Margin Impact', fontsize=14, weight='bold', pad=15)
    plt.xlabel('Sum of Quantity Ordered', fontsize=12, weight='bold')
    plt.ylabel('Sum of Total Profit ($)', fontsize=12, weight='bold')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Custom legend construction for the mapping colors
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], marker='o', color='w', label=key, 
                              markerfacecolor=val, markersize=12, markeredgecolor='black') 
                       for key, val in color_map.items()]
    plt.legend(handles=legend_elements, title="Order Priority", loc="upper left")
    
    plt.tight_layout()
    plt.savefig('outputs/charts/fulfillment_operational_matrix.png', dpi=300)
    plt.close()
    
    print("\nSUCCESS: All analytical charts exported directly into the outputs folder!")

if __name__ == '__main__':
    export_all_charts_simple()