# Save merged data
merged_columns_to_save = [
    'Primary Key', 'Order No', 'Order Date', 'Manufacturer', 'Product Category',
    'Model Year', 'Serial Number', 'Complaint', 'Correction', 
    'Failure Condition - Failure Component', 'Fix Condition - Fix Component',
    'Part Description', 'Revenue', 'Cost_Numeric', 'Actual Hours', 
    'Cost_Per_Hour', 'Year', 'Month'
]

df_merged_final = df_merged[merged_columns_to_save].copy()
df_merged_final.rename(columns={'Cost_Numeric': 'Cost'}, inplace=True)
df_merged_final.to_csv('data/processed/task2_merged_dataset.csv', index=False)

print(" Task 2 merged data saved as 'data/processed/task2_merged_dataset.csv'")
print(f"Merged dataset shape: {df_merged_final.shape}")

# ===============================================================================
# TASK 3: EXPLORATORY DATA ANALYSIS - COMPLETE IMPLEMENTATION  
# ===============================================================================

print("\n" + "="*80)
print("TASK 3: EXPLORATORY DATA ANALYSIS")
print("="*80)

# 1. TREND ANALYSIS
print("\n1. TREND ANALYSIS")
print("-" * 50)

# Cost vs Hours Correlation Analysis
print("Cost vs Actual Hours Correlation:")
# Filter out zero hours and negative costs for meaningful correlation
df_analysis = df_merged[(df_merged['Actual Hours'] > 0) & (df_merged['Cost_Numeric'] >= 0)].copy()
cost_hours_corr = df_analysis['Cost_Numeric'].corr(df_analysis['Actual Hours'])
print(f"Correlation coefficient: {cost_hours_corr:.3f}")

if abs(cost_hours_corr) > 0.5:
    correlation_strength = "Strong"
elif abs(cost_hours_corr) > 0.3:
    correlation_strength = "Moderate"
else:
    correlation_strength = "Weak"
    
print(f"Interpretation: {correlation_strength} {'positive' if cost_hours_corr > 0 else 'negative'} correlation")

# Yearly trend analysis
print(f"\nYearly Trends:")
yearly_analysis = df_merged.groupby('Year').agg({
    'Cost_Numeric': ['sum', 'mean', 'count'],
    'Actual Hours': ['sum', 'mean'],
    'Revenue': 'sum'
}).round(2)

yearly_analysis.columns = ['Total_Cost', 'Avg_Cost', 'Repair_Count', 'Total_Hours', 'Avg_Hours', 'Total_Revenue']
print(yearly_analysis)

# Product category analysis
print(f"\nProduct Category Analysis:")
category_analysis = df_merged.groupby('Product Category').agg({
    'Cost_Numeric': ['mean', 'sum', 'count', 'min', 'max'],
    'Actual Hours': ['mean', 'sum'],
    'Cost_Per_Hour': 'mean'
}).round(2)

category_analysis.columns = ['Avg_Cost', 'Total_Cost', 'Count', 'Min_Cost', 'Max_Cost', 'Avg_Hours', 'Total_Hours', 'Avg_Cost_Per_Hour']
print(category_analysis)

# Manufacturer analysis
print(f"\nManufacturer Analysis:")
manufacturer_analysis = df_merged.groupby('Manufacturer').agg({
    'Cost_Numeric': ['mean', 'sum', 'count'],
    'Actual Hours': ['mean']
}).round(2)
manufacturer_analysis.columns = ['Avg_Cost', 'Total_Cost', 'Count', 'Avg_Hours']
print(manufacturer_analysis)