# 2. DATA CLEANING
print("\n2. DATA CLEANING")
print("-" * 50)

# Create copies for cleaning
df_work_orders_clean = df_work_orders.copy()
df_repair_data_clean = df_repair_data.copy()

print("Cleaning Work Order Data:")
print("Before cleaning - Missing values:")
wo_missing_before = df_work_orders_clean.isnull().sum()
print(wo_missing_before[wo_missing_before > 0])

# Clean Work Orders
# Convert date columns
df_work_orders_clean['Order Date'] = pd.to_datetime(df_work_orders_clean['Order Date'])
print(" Order Date converted to datetime")

# Handle missing values in Cause (appears to be mostly empty)
df_work_orders_clean['Cause'] = df_work_orders_clean['Cause'].fillna('Not Specified')
print(" Missing Cause values filled with 'Not Specified'")

# Standardize text columns
df_work_orders_clean['Complaint_Clean'] = df_work_orders_clean['Complaint'].str.strip()
df_work_orders_clean['Correction_Clean'] = df_work_orders_clean['Correction'].str.strip()
print(" Text fields standardized")

# Handle Model Year (0 likely means unknown/not applicable)
model_year_zero = (df_work_orders_clean['Model Year'] == 0).sum()
print(f" Model Year: {model_year_zero} records with value 0 (likely indicates N/A)")

print("\nCleaning Repair Data:")
print("Before cleaning - Missing values:")
rd_missing_before = df_repair_data_clean.isnull().sum()
print(rd_missing_before[rd_missing_before > 0])

# Clean cost columns - handle different formats
def clean_currency_column(value):
    if pd.isna(value):
        return 0.0
    if isinstance(value, str):
        # Remove $ and convert to float
        cleaned = value.replace('$', '').replace(',', '').strip()
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    return float(value)

# Clean Cost column
df_repair_data_clean['Cost_Numeric'] = df_repair_data_clean['Cost'].apply(clean_currency_column)
print(" Cost column converted to numeric")

# Clean Segment Total column  
df_repair_data_clean['Segment_Total_Numeric'] = df_repair_data_clean['Segment Total $'].apply(clean_currency_column)
print(" Segment Total converted to numeric")

# Handle missing Coverage
df_repair_data_clean['Coverage'] = df_repair_data_clean['Coverage'].fillna('Not Specified')
print(" Missing Coverage values handled")

# Clean Part Description
df_repair_data_clean['Part_Description_Clean'] = df_repair_data_clean['Part Description'].str.strip()
print(" Part descriptions cleaned")

# Flag negative quantities (returns/cores)
df_repair_data_clean['Is_Return'] = df_repair_data_clean['Qty'] < 0
negative_qty_count = df_repair_data_clean['Is_Return'].sum()
print(f" {negative_qty_count} return/core transactions flagged")

print(f"\nCleaning Summary:")
print(f"Work Orders after cleaning: {df_work_orders_clean.shape}")
print(f"Repair Data after cleaning: {df_repair_data_clean.shape}")

# Check final missing values
print("\nFinal missing values check:")
wo_missing_after = df_work_orders_clean.isnull().sum()
rd_missing_after = df_repair_data_clean.isnull().sum()

if wo_missing_after.sum() > 0:
    print("Work Orders remaining missing:")
    print(wo_missing_after[wo_missing_after > 0])
else:
    print(" Work Orders: No missing values")
    
if rd_missing_after.sum() > 0:
    print("Repair Data remaining missing:")
    print(rd_missing_after[rd_missing_after > 0])
else:
    print(" Repair Data: No missing values")