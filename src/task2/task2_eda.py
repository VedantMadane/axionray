# ===============================================================================
# TASK 2: DATA PREPARATION AND INTEGRATION - COMPLETE IMPLEMENTATION
# ===============================================================================

print("="*80)
print("TASK 2: DATA PREPARATION AND INTEGRATION")
print("="*80)

# 1. PRIMARY KEY IDENTIFICATION
print("\n1. PRIMARY KEY IDENTIFICATION")
print("-" * 50)

print(f"Work Order Data shape: {df_work_orders.shape}")
print(f"Repair Data shape: {df_repair_data.shape}")

# Analyze primary key candidates
print("\nPrimary Key Analysis:")
print(f"Work Orders 'Primary Key' unique values: {df_work_orders['Primary Key'].nunique()} out of {len(df_work_orders)}")
print(f"Repair Data 'Primary Key' unique values: {df_repair_data['Primary Key'].nunique()} out of {len(df_repair_data)}")

# Check overlap
wo_keys = set(df_work_orders['Primary Key'])
rd_keys = set(df_repair_data['Primary Key'])
common_keys = wo_keys.intersection(rd_keys)

print(f"Common Primary Keys: {len(common_keys)}")
print(f"Work Orders only: {len(wo_keys - rd_keys)}")
print(f"Repair Data only: {len(rd_keys - wo_keys)}")

print("\nPrimary Key Selection: 'Primary Key'")
print("Justification:")
print("• Explicitly named as Primary Key in both datasets")
print("• Format: 'SO[ORDER_NUMBER]-[SEGMENT_NUMBER]' ensures uniqueness")
print("• Present in both datasets with 495 matching values")
print("• Enables linking work order details with repair costs/parts")

# Check for potential issues
print(f"\nPotential Challenges:")
duplicate_wo = df_work_orders['Primary Key'].duplicated().sum()
duplicate_rd = df_repair_data['Primary Key'].duplicated().sum()
print(f"• Duplicate Primary Keys in Work Orders: {duplicate_wo}")
print(f"• Duplicate Primary Keys in Repair Data: {duplicate_rd}")
if len(wo_keys - rd_keys) > 0:
    print(f"• {len(wo_keys - rd_keys)} work orders without repair data")
if len(rd_keys - wo_keys) > 0:
    print(f"• {len(rd_keys - wo_keys)} repair records without work orders")