import pandas as pd
# Load the Task 2 dataset (SA-Data-for-Task-2.xlsx)
print("=== LOADING TASK 2 DATASET ===")
try:
    # Load Work Order Data
    df_work_orders = pd.read_excel('data/raw/SA-Data-for-Task-2.xlsx', sheet_name='Work Order Data')
    print(f" Work Order Data loaded successfully")
    print(f"Work Order Data shape: {df_work_orders.shape}")
    print(f"Work Order columns: {list(df_work_orders.columns)}")
    
    # Load Repair Data  
    df_repair_data = pd.read_excel('data/raw/SA-Data-for-Task-2.xlsx', sheet_name='Repair Data')
    print(f" Repair Data loaded successfully") 
    print(f"Repair Data shape: {df_repair_data.shape}")
    print(f"Repair Data columns: {list(df_repair_data.columns)}")
    
    print("\n=== WORK ORDER DATA SAMPLE ===")
    print(df_work_orders.head(2))
    
    print("\n=== REPAIR DATA SAMPLE ===")
    print(df_repair_data.head(2))
    
    # Check primary key candidates
    print(f"\nWork Order 'Primary Key' unique values: {df_work_orders['Primary Key'].nunique()} out of {len(df_work_orders)}")
    print(f"Repair Data 'Primary Key' unique values: {df_repair_data['Primary Key'].nunique()} out of {len(df_repair_data)}")
    print(f"Common Primary Keys: {len(set(df_work_orders['Primary Key']).intersection(set(df_repair_data['Primary Key'])))}")
    
except Exception as e:
    print(f"Error loading Task 2 data: {e}")
    df_work_orders = None
    df_repair_data = None
