# 2. DATA CLEANING
print("\n2. DATA CLEANING")
print("-" * 50)

# Create a copy for cleaning
df_task1_cleaned = df_task1.copy()

# Handle missing values
print("Missing values handling:")
print("Before cleaning:")
missing_before = df_task1_cleaned.isnull().sum()
print(missing_before[missing_before > 0])

# Fill missing CAUSAL_PART_NM with 'UNKNOWN'
df_task1_cleaned['CAUSAL_PART_NM'] = df_task1_cleaned['CAUSAL_PART_NM'].fillna('UNKNOWN')

# Fill other missing values with appropriate defaults
df_task1_cleaned['PLANT'] = df_task1_cleaned['PLANT'].fillna('UNKNOWN')
df_task1_cleaned['STATE'] = df_task1_cleaned['STATE'].fillna('UNKNOWN')
df_task1_cleaned['REPAIR_DLR_POSTAL_CD'] = df_task1_cleaned['REPAIR_DLR_POSTAL_CD'].fillna('00000')
df_task1_cleaned['VEH_TEST_GRP'] = df_task1_cleaned['VEH_TEST_GRP'].fillna('UNKNOWN')
df_task1_cleaned['OPTN_FAMLY_CERTIFICATION'] = df_task1_cleaned['OPTN_FAMLY_CERTIFICATION'].fillna('NONE')
df_task1_cleaned['OPTF_FAMLY_EMISSIOF_SYSTEM'] = df_task1_cleaned['OPTF_FAMLY_EMISSIOF_SYSTEM'].fillna('NONE')

# Handle engine and transmission missing values
engine_cols = ['ENGINE_SOURCE_PLANT', 'ENGINE_TRACE_NBR', 'TRANSMISSION_SOURCE_PLANT', 'TRANSMISSION_TRACE_NBR']
for col in engine_cols:
    if col in df_task1_cleaned.columns:
        df_task1_cleaned[col] = df_task1_cleaned[col].fillna('UNKNOWN')

# Fill LINE_SERIES and LAST_KNOWN_DELVRY_TYPE_CD
df_task1_cleaned['LINE_SERIES'] = df_task1_cleaned['LINE_SERIES'].fillna('UNKNOWN')
df_task1_cleaned['LAST_KNOWN_DELVRY_TYPE_CD'] = df_task1_cleaned['LAST_KNOWN_DELVRY_TYPE_CD'].fillna(0)

print("After cleaning:")
missing_after = df_task1_cleaned.isnull().sum()
print(missing_after[missing_after > 0])

# Text standardization
print("\nText standardization:")
df_task1_cleaned['CUSTOMER_VERBATIM_CLEAN'] = df_task1_cleaned['CUSTOMER_VERBATIM'].str.upper().str.strip()
df_task1_cleaned['CORRECTION_VERBATIM_CLEAN'] = df_task1_cleaned['CORRECTION_VERBATIM'].str.upper().str.strip()
df_task1_cleaned['CAUSAL_PART_NM_CLEAN'] = df_task1_cleaned['CAUSAL_PART_NM'].str.upper().str.strip()
print(" Text fields standardized to uppercase and stripped")

# Create cost severity categories
def categorize_cost_severity(cost):
    if cost < 100:
        return 'LOW'
    elif cost < 500:
        return 'MEDIUM'
    elif cost < 1500:
        return 'HIGH'
    else:
        return 'CRITICAL'

df_task1_cleaned['COST_SEVERITY'] = df_task1_cleaned['TOTALCOST'].apply(categorize_cost_severity)

# Create warranty status categories
def categorize_warranty_status(age):
    if age <= 1:
        return 'NEW_VEHICLE'
    elif age <= 3:
        return 'BASIC_WARRANTY'
    elif age <= 5:
        return 'EXTENDED_WARRANTY'
    else:
        return 'OUT_OF_WARRANTY'

df_task1_cleaned['WARRANTY_STATUS'] = df_task1_cleaned['REPAIR_AGE'].apply(categorize_warranty_status)

print(" Cost severity and warranty status categories created")
print(f"Cost severity distribution: {df_task1_cleaned['COST_SEVERITY'].value_counts().to_dict()}")
print(f"Warranty status distribution: {df_task1_cleaned['WARRANTY_STATUS'].value_counts().to_dict()}")
