# Handle remaining missing values
print("Handling remaining missing values:")

# Fill missing Correction with placeholder
df_work_orders_clean['Correction'] = df_work_orders_clean['Correction'].fillna('No correction details provided')
df_work_orders_clean['Correction_Clean'] = df_work_orders_clean['Correction_Clean'].fillna('No correction details provided')
print(" Missing Correction values filled")

# Fill missing Actual Hours with 0 (assuming no labor time recorded)
df_repair_data_clean['Actual Hours'] = df_repair_data_clean['Actual Hours'].fillna(0.0)
print(" Missing Actual Hours filled with 0")

# Final verification
wo_final_missing = df_work_orders_clean.isnull().sum().sum()
rd_final_missing = df_repair_data_clean.isnull().sum().sum()
print(f"Final missing values - Work Orders: {wo_final_missing}, Repair Data: {rd_final_missing}")

# 3. DATA INTEGRATION
print("\n3. DATA INTEGRATION")
print("-" * 50)

print("Join Type Selection: INNER JOIN")
print("Rationale:")
print("• Ensures complete records with both work order and repair information")
print("• Only includes records where we have both complaint details and cost data")
print("• Eliminates incomplete records that could skew analysis")
print("• Provides reliable dataset for trend analysis")

# Perform inner join
df_merged = pd.merge(
    df_work_orders_clean, 
    df_repair_data_clean, 
    on='Primary Key', 
    how='inner',
    suffixes=('_WO', '_RD')
)

print(f"\n Integration successful!")
print(f"Merged dataset shape: {df_merged.shape}")
print(f"Records successfully merged: {len(df_merged)}")

# Join type implications
print("\nJoin Type Analysis:")
print("Inner Join (SELECTED):")
print("  Complete data for analysis")
print("  Reliable cost-complaint relationships")
print("    Loses 5 work orders without repair data")

print("\nAlternative Join Types:")
print("Left Join:")
print("  Retains all work orders")
print("    Creates null values in repair data")
print("    Complicates cost analysis")

print("Right Join:")
print("  Retains all repair records")  
print("    May include orphaned parts")
print("    Less useful for complaint analysis")

# Analyze merged data
print(f"\nMerged Dataset Analysis:")
print(f"Date range: {df_merged['Order Date'].min()} to {df_merged['Order Date'].max()}")
print(f"Product categories: {df_merged['Product Category'].unique()}")
print(f"Manufacturers: {df_merged['Manufacturer'].unique()}")
print(f"Total cost range: ${df_merged['Cost_Numeric'].min():.2f} to ${df_merged['Cost_Numeric'].max():.2f}")
print(f"Total revenue: ${df_merged['Revenue'].sum():.2f}")
print(f"Total labor hours: {df_merged['Actual Hours'].sum():.1f}")

# Create additional derived columns for analysis
df_merged['Cost_Per_Hour'] = df_merged['Cost_Numeric'] / (df_merged['Actual Hours'] + 0.1)  # Add small value to avoid division by zero
df_merged['Year'] = df_merged['Order Date'].dt.year
df_merged['Month'] = df_merged['Order Date'].dt.month

print(f" Added derived columns: Cost_Per_Hour, Year, Month")