# 2. ROOT CAUSE IDENTIFICATION
print("\n2. ROOT CAUSE IDENTIFICATION")
print("-" * 50)

# Failure condition analysis
print("Top Failure Conditions:")
failure_conditions = df_merged['Failure Condition - Failure Component'].value_counts().head(10)
for condition, count in failure_conditions.items():
    print(f"  {condition}: {count}")

# Fix condition analysis  
print(f"\nTop Fix Actions:")
fix_conditions = df_merged['Fix Condition - Fix Component'].value_counts().head(10)
for condition, count in fix_conditions.items():
    print(f"  {condition}: {count}")

# Extract component types for analysis
def extract_component_from_failure(failure_condition):
    if pd.isna(failure_condition):
        return 'Unknown'
    parts = str(failure_condition).split(' - ')
    if len(parts) > 1:
        return parts[1].strip()
    return 'Not Mentioned'

df_merged['Failed_Component'] = df_merged['Failure Condition - Failure Component'].apply(extract_component_from_failure)

print(f"\nComponent Failure Analysis:")
component_failures = df_merged['Failed_Component'].value_counts().head(8)
for component, count in component_failures.items():
    print(f"  {component}: {count}")

# Cost impact by component
print(f"\nCost Impact by Failed Component:")
component_cost_impact = df_merged.groupby('Failed_Component').agg({
    'Cost_Numeric': ['mean', 'sum', 'count'],
    'Actual Hours': ['mean', 'sum']
}).round(2)

component_cost_impact.columns = ['Avg_Cost', 'Total_Cost', 'Count', 'Avg_Hours', 'Total_Hours']
# Show top components by count
top_components = component_failures.head(8).index
print(component_cost_impact.loc[top_components])

# High-cost repairs analysis
print(f"\nHigh-Cost Repair Analysis (>$1000):")
high_cost_repairs = df_merged[df_merged['Cost_Numeric'] > 1000]
print(f"High-cost repairs: {len(high_cost_repairs)} out of {len(df_merged)} ({len(high_cost_repairs)/len(df_merged)*100:.1f}%)")

if len(high_cost_repairs) > 0:
    print("Top high-cost failure types:")
    high_cost_components = high_cost_repairs['Failed_Component'].value_counts()
    for component, count in high_cost_components.items():
        avg_cost = high_cost_repairs[high_cost_repairs['Failed_Component'] == component]['Cost_Numeric'].mean()
        print(f"  {component}: {count} cases, avg ${avg_cost:.2f}")

# Efficiency analysis - cost per hour by component
print(f"\nRepair Efficiency by Component (Cost per Hour):")
# Filter components with meaningful hours (>0) 
efficiency_data = df_merged[df_merged['Actual Hours'] > 0].groupby('Failed_Component').agg({
    'Cost_Per_Hour': 'mean',
    'Cost_Numeric': 'mean',
    'Actual Hours': 'mean'
}).round(2)

efficiency_data = efficiency_data.sort_values('Cost_Per_Hour', ascending=True)
print(efficiency_data.head(8))

print("\n3. KEY INSIGHTS FOR STAKEHOLDERS")
print("-" * 50)

print("    OPERATIONAL INSIGHTS:")
most_common_failure = component_failures.index[0]
most_expensive_component = component_cost_impact.loc[component_cost_impact['Avg_Cost'].idxmax()]
most_labor_intensive = component_cost_impact.loc[component_cost_impact['Avg_Hours'].idxmax()]

print(f"• Most common failure: {most_common_failure} ({component_failures.iloc[0]} cases)")
print(f"• Highest average cost component: {component_cost_impact['Avg_Cost'].idxmax()} (${component_cost_impact['Avg_Cost'].max():.2f})")
print(f"• Most labor-intensive: {component_cost_impact['Avg_Hours'].idxmax()} ({component_cost_impact['Avg_Hours'].max():.1f} hrs avg)")

print(f"\n💰 FINANCIAL INSIGHTS:")
print(f"• Profit margin is healthy at {profit_margin:.1f}%")
print(f"• SPRAYS category drives {(87377.37/119821.25)*100:.1f}% of total costs but generates significant revenue")
print(f"• Average repair cost varies significantly by product: ${category_analysis['Avg_Cost'].min():.2f} - ${category_analysis['Avg_Cost'].max():.2f}")

print(f"\n⚡ EFFICIENCY INSIGHTS:")
print(f"• Weak correlation between cost and hours suggests standardization opportunities")
print(f"• {len(high_cost_repairs)} high-cost repairs (>${1000}) need special attention")
print(f"• Cost per hour varies significantly across components: need process optimization")