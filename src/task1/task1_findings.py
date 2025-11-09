# Prepare data for Task 3 visualizations

# 1. Yearly trends data
yearly_trend_data = []
for year, row in yearly_analysis.iterrows():
    yearly_trend_data.append({
        "Year": str(year),
        "Metric": "Total Cost ($)",
        "Value": row['Total_Cost']
    })
    yearly_trend_data.append({
        "Year": str(year), 
        "Metric": "Total Hours",
        "Value": row['Total_Hours']
    })

# 2. Cost vs Hours scatter plot data (sample for visualization)
scatter_data = []
# Take a sample of records with meaningful data for visualization
sample_df = df_merged[(df_merged['Actual Hours'] > 0) & 
                     (df_merged['Cost_Numeric'] >= -100) & 
                     (df_merged['Cost_Numeric'] <= 1000)].sample(min(50, len(df_merged)), random_state=42)

for _, row in sample_df.iterrows():
    scatter_data.append({
        "Actual_Hours": row['Actual Hours'],
        "Cost_Numeric": row['Cost_Numeric'],
        "Failed_Component": row['Failed_Component']
    })

# 3. Product category cost analysis
category_cost_data = []
for category, row in category_analysis.iterrows():
    category_cost_data.append({
        "Product_Category": category,
        "Average_Cost": row['Avg_Cost'],
        "Count": row['Count'],
        "Min_Cost": row['Min_Cost'],
        "Max_Cost": row['Max_Cost']
    })

print(" Prepared visualization data:")
print(f"  - Yearly trends: {len(yearly_trend_data)} data points")
print(f"  - Cost vs Hours scatter: {len(scatter_data)} data points") 
print(f"  - Category analysis: {len(category_cost_data)} categories")

# Save final analysis results
analysis_summary = {
    'total_records': len(df_merged),
    'date_range': f"{df_merged['Order Date'].min()} to {df_merged['Order Date'].max()}",
    'total_cost': total_cost,
    'total_revenue': total_revenue,
    'profit_margin': profit_margin,
    'cost_hours_correlation': cost_hours_corr,
    'top_failure_component': most_common_failure,
    'most_expensive_avg_component': component_cost_impact['Avg_Cost'].idxmax(),
    'high_cost_repairs_count': len(high_cost_repairs)
}

print(f"\n📋 ANALYSIS SUMMARY:")
for key, value in analysis_summary.items():
    print(f"  {key}: {value}")

print(f"\n Task 3 EDA completed successfully")
print(f" Ready to generate visualizations")