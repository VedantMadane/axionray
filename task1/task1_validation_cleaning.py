# ===============================================================================
# TASK 1: DATA VALIDATION AND CLEANING - COMPLETE IMPLEMENTATION
# ===============================================================================

print("="*80)
print("TASK 1: DATA VALIDATION AND CLEANING")
print("="*80)

# 1. COLUMN-WISE ANALYSIS
print("\n1. COLUMN-WISE ANALYSIS")
print("-" * 50)

# Select top 5 critical columns based on business impact
critical_columns = {
    'CAUSAL_PART_NM': 'Root cause component - critical for failure analysis',
    'TOTALCOST': 'Financial impact - critical for cost management',
    'CUSTOMER_VERBATIM': 'Customer complaint - critical for user experience',
    'REPAIR_AGE': 'Vehicle age at repair - warranty and reliability analysis', 
    'CORRECTION_VERBATIM': 'Repair action taken - operational insights'
}

print("Top 5 Critical Columns:")
for i, (col, description) in enumerate(critical_columns.items(), 1):
    print(f"{i}. {col}: {description}")

# Detailed analysis of critical columns
print("\nDetailed Column Analysis:")
for col in critical_columns.keys():
    print(f"\n{col}:")
    print(f"  Data type: {df_task1[col].dtype}")
    print(f"  Unique values: {df_task1[col].nunique()}")
    print(f"  Missing values: {df_task1[col].isnull().sum()}")
    if df_task1[col].dtype in ['int64', 'float64']:
        print(f"  Range: {df_task1[col].min():.2f} - {df_task1[col].max():.2f}")
        print(f"  Mean: {df_task1[col].mean():.2f}")
    else:
        print(f"  Sample values: {df_task1[col].dropna().unique()[:3]}")

print("\nNumerical Columns Statistics:")
numerical_cols = ['TOTALCOST', 'LBRCOST', 'REPORTING_COST', 'REPAIR_AGE', 'KM']
print(df_task1[numerical_cols].describe())