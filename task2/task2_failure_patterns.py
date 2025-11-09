# Check column names in merged dataframe
print("Merged dataframe columns:")
print(list(df_merged.columns))

# Find columns that match our requirements
available_columns = []
required_base_names = [
    'Primary Key', 'Order No', 'Order Date', 'Manufacturer', 'Product Category',
    'Model Year', 'Serial Number', 'Complaint', 'Correction', 
    'Failure Condition - Failure Component', 'Fix Condition - Fix Component',
    'Part Description', 'Revenue', 'Cost_Numeric', 'Actual Hours', 
    'Cost_Per_Hour', 'Year', 'Month'
]

for col in df_merged.columns:
    for req_col in required_base_names:
        if req_col in col or col == req_col:
            available_columns.append(col)
            break

print(f"\nAvailable columns matching requirements:")
for col in available_columns:
    print(f"  {col}")

# Use available columns to save merged data
df_merged_final = df_merged[available_columns].copy()

# Rename columns to remove suffixes for cleaner export
rename_mapping = {}
for col in df_merged_final.columns:
    if '_WO' in col:
        rename_mapping[col] = col.replace('_WO', '')
    elif '_RD' in col:
        rename_mapping[col] = col.replace('_RD', '')

if rename_mapping:
    df_merged_final.rename(columns=rename_mapping, inplace=True)

# Rename Cost_Numeric to Cost for clarity
if 'Cost_Numeric' in df_merged_final.columns:
    df_merged_final.rename(columns={'Cost_Numeric': 'Cost'}, inplace=True)

df_merged_final.to_csv('data/processed/task2_merged_dataset.csv', index=False)

print(f"\n Task 2 merged data saved as 'data/processed/task2_merged_dataset.csv'")
print(f"Merged dataset shape: {df_merged_final.shape}")
print(f"Final column names: {list(df_merged_final.columns)}")