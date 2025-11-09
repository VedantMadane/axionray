# ===============================================================================
# TASK 3: EXPLORATORY DATA ANALYSIS - COMPLETE IMPLEMENTATION  
# ===============================================================================

print("="*80)
print("TASK 3: EXPLORATORY DATA ANALYSIS")
print("="*80)

# 1. TREND ANALYSIS
print("\n1. TREND ANALYSIS")
print("-" * 50)

# Cost vs Hours Correlation Analysis
print("Cost vs Actual Hours Correlation:")
# Filter out zero hours and extreme negative costs for meaningful correlation
df_analysis = df_merged[(df_merged['Actual Hours'] > 0) & (df_merged['Cost_Numeric'] > -1000)].copy()
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
    'Actual Hours': ['mean', 'sum']
}).round(2)

category_analysis.columns = ['Avg_Cost', 'Total_Cost', 'Count', 'Min_Cost', 'Max_Cost', 'Avg_Hours', 'Total_Hours']
print(category_analysis)

# Manufacturer analysis
print(f"\nManufacturer Analysis:")
manufacturer_analysis = df_merged.groupby('Manufacturer').agg({
    'Cost_Numeric': ['mean', 'sum', 'count'],
    'Actual Hours': ['mean']
}).round(2)
manufacturer_analysis.columns = ['Avg_Cost', 'Total_Cost', 'Count', 'Avg_Hours']
print(manufacturer_analysis)

# Financial metrics
print(f"\nKey Financial Metrics:")
total_cost = df_merged['Cost_Numeric'].sum()
total_revenue = df_merged['Revenue'].sum()
profit_margin = ((total_revenue - total_cost) / total_revenue * 100) if total_revenue != 0 else 0
total_hours = df_merged['Actual Hours'].sum()
avg_cost_per_hour = df_merged['Cost_Numeric'].sum() / df_merged['Actual Hours'].sum()

print(f"• Total repair costs: ${total_cost:,.2f}")
print(f"• Total revenue: ${total_revenue:,.2f}")
print(f"• Profit margin: {profit_margin:.1f}%")
print(f"• Total labor hours: {total_hours:,.1f}")
print(f"• Average cost per hour: ${avg_cost_per_hour:.2f}")