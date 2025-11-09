# Save cleaned Task 1 data
task1_columns_to_save = [
    'VIN', 'TRANSACTION_ID', 'REPAIR_DATE', 'CUSTOMER_VERBATIM', 'CORRECTION_VERBATIM',
    'CAUSAL_PART_NM', 'TOTALCOST', 'LBRCOST', 'REPAIR_AGE', 'KM', 'BUILD_COUNTRY', 
    'PLATFORM', 'ENGINE', 'COST_SEVERITY', 'WARRANTY_STATUS', 'FAILURE_SYMPTOMS_STR',
    'REPAIR_ACTIONS_STR', 'COMPONENT_CATEGORY'
]

df_task1_final = df_task1_cleaned[task1_columns_to_save].copy()
df_task1_final.to_csv('data/processed/task1_cleaned_tagged_steering_data.csv', index=False)

print(" Task 1 cleaned data saved as 'data/processed/task1_cleaned_tagged_steering_data.csv'")
print(f"Final dataset shape: {df_task1_final.shape}")

# Prepare data for visualizations
print("\nPreparing visualization data...")

# Data for failure symptoms chart
failure_symptom_data = []
for symptom, count in symptom_counts.most_common():
    if symptom != 'OTHER':  # Exclude 'OTHER' for cleaner visualization
        failure_symptom_data.append({'Symptom': symptom, 'Count': count})

# Data for cost severity distribution
cost_severity_data = []
cost_severity_dist = df_task1_cleaned['COST_SEVERITY'].value_counts()
for severity, count in cost_severity_dist.items():
    cost_severity_data.append({'Cost_Severity': severity, 'Count': count})

# Data for age vs cost analysis
age_cost_data = []
for _, row in df_task1_cleaned.iterrows():
    age_cost_data.append({
        'Vehicle_Age': row['REPAIR_AGE'],
        'Total_Cost': row['TOTALCOST']
    })

print(f" Prepared data for {len(failure_symptom_data)} failure symptoms")
print(f" Prepared data for {len(cost_severity_data)} cost severity levels")
print(f" Prepared data for {len(age_cost_data)} age vs cost points")

print("\n" + "="*80)
print("TASK 1 SUMMARY")
print("="*80)
print(f"• Total records processed: {len(df_task1_cleaned)}")
print(f"• Missing values handled: {missing_before.sum()} → {missing_after.sum()}")
print(f"• Generated tags: Failure symptoms, Repair actions, Component categories")
print(f"• Created derived features: Cost severity, Warranty status")
print(f"• Most common failure: {symptom_counts.most_common(1)[0][0]} ({symptom_counts.most_common(1)[0][1]} cases)")
print(f"• Most common repair: {action_counts.most_common(1)[0][0]} ({action_counts.most_common(1)[0][1]} cases)")
print(f"• Average repair cost: ${df_task1_cleaned['TOTALCOST'].mean():.2f}")
print(f"• Cost range: ${df_task1_cleaned['TOTALCOST'].min():.2f} - ${df_task1_cleaned['TOTALCOST'].max():.2f}")