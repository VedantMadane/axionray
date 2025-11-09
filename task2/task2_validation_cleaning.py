# 3. GENERATING TAGS/FEATURES FROM FREE TEXT
print("\n3. GENERATING TAGS FROM FREE TEXT FIELDS")
print("-" * 50)

# Function to extract failure symptoms from customer complaints
def extract_failure_symptoms(text):
    symptoms = []
    if pd.isna(text):
        return ['UNKNOWN']
    
    text_upper = str(text).upper()
    
    # Material degradation symptoms
    if any(word in text_upper for word in ['COMING APART', 'COMING OFF', 'PEELING', 'STITCHING', 'TEAR', 'RIP', 'FRAY']):
        symptoms.append('MATERIAL_DEGRADATION')
    
    # Functional failure symptoms  
    if any(word in text_upper for word in ['NOT WORK', 'INOP', 'INOPERATIVE', 'FAILS', 'BROKEN', 'MALFUNCTION', 'WON\'T', 'WONT']):
        symptoms.append('FUNCTIONAL_FAILURE')
        
    # Noise issues
    if any(word in text_upper for word in ['NOISE', 'RUBBING', 'CLICKING', 'SOUND', 'SQUEAK', 'RATTLE']):
        symptoms.append('NOISE_ISSUE')
        
    # Temperature regulation issues (expanded from just heating)
    if any(word in text_upper for word in ['HEAT', 'TEMP', 'COLD', 'HOT', 'WARM', 'COOL', 'THERMOSTAT']):
        symptoms.append('TEMPERATURE_ISSUE')
        
    # Warning system issues
    if any(word in text_upper for word in ['MESSAGE', 'WARNING', 'LIGHT', 'DASH', 'ALERT', 'DTC', 'CODE']):
        symptoms.append('WARNING_SYSTEM')
        
    # Driver assistance issues
    if any(word in text_upper for word in ['CRUISE', 'ASSIST', 'DRIVER', 'SUPER CRUISE', 'LANE', 'AUTO']):
        symptoms.append('DRIVER_ASSISTANCE')
        
    # Fluid issues
    if any(word in text_upper for word in ['OIL', 'COOLANT', 'FLUID', 'LEAK', 'LOW', 'LOST', 'LOSING']):
        if any(word in text_upper for word in ['OIL', 'COOLANT', 'FLUID']):
            symptoms.append('FLUID_ISSUE')
    
    # Mechanical wear
    if any(word in text_upper for word in ['BELT', 'BEARING', 'CHAIN', 'PULLEY']):
        symptoms.append('MECHANICAL_WEAR')
        
    # Electrical issues
    if any(word in text_upper for word in ['SHORT', 'WIRE', 'WIRING', 'ELECTRICAL', 'FUSE', 'CIRCUIT']):
        symptoms.append('ELECTRICAL_ISSUE')
    
    # Performance issues
    if any(word in text_upper for word in ['POWER', 'PERFORMANCE', 'ACCELERATION', 'STALL', 'STALLING']):
        symptoms.append('PERFORMANCE_ISSUE')
    
    # If no specific symptoms found but contains common issue indicators
    if not symptoms and any(word in text_upper for word in ['ISSUE', 'PROBLEM', 'CONCERN', 'TROUBLE']):
        symptoms.append('GENERAL_ISSUE')
    
    return symptoms if symptoms else ['OTHER']

# Function to extract repair actions from correction verbatim
def extract_repair_actions(text):
    actions = []
    if pd.isna(text):
        return ['UNKNOWN']
        
    text_upper = str(text).upper()
    
    if any(word in text_upper for word in ['REPLACED', 'REPLACE']):
        actions.append('REPLACEMENT')
    if any(word in text_upper for word in ['ADJUSTED', 'ADJUST']):
        actions.append('ADJUSTMENT') 
    if any(word in text_upper for word in ['REPAIRED', 'REPAIR', 'FIXED']):
        actions.append('REPAIR')
    if any(word in text_upper for word in ['PROGRAMMED', 'PROGRAMMING', 'SOFTWARE']):
        actions.append('SOFTWARE_UPDATE')
    if any(word in text_upper for word in ['DIAGNOSED', 'DIAGNOSTIC', 'TESTED']):
        actions.append('DIAGNOSTIC')
        
    return actions if actions else ['OTHER']

# Function to extract component categories
def extract_component_category(part_name):
    if pd.isna(part_name) or part_name == 'UNKNOWN':
        return 'UNKNOWN'
    
    part_upper = str(part_name).upper()
    
    if 'WHEEL' in part_upper and 'STRG' in part_upper:
        return 'STEERING_WHEEL_ASSEMBLY'
    elif 'MODULE' in part_upper and ('HT' in part_upper or 'HEAT' in part_upper):
        return 'HEATING_MODULE'  
    elif 'HARNESS' in part_upper:
        return 'WIRING_HARNESS'
    elif 'WHEEL ASM' in part_upper:
        return 'STEERING_WHEEL_ASSEMBLY'
    else:
        return 'OTHER_COMPONENT'

# Apply tag extraction functions
df_task1_cleaned['FAILURE_SYMPTOMS'] = df_task1_cleaned['CUSTOMER_VERBATIM'].apply(extract_failure_symptoms)
df_task1_cleaned['REPAIR_ACTIONS'] = df_task1_cleaned['CORRECTION_VERBATIM'].apply(extract_repair_actions)
df_task1_cleaned['COMPONENT_CATEGORY'] = df_task1_cleaned['CAUSAL_PART_NM'].apply(extract_component_category)

# Create flattened symptom and action counts
all_symptoms = []
all_actions = []

for symptom_list in df_task1_cleaned['FAILURE_SYMPTOMS']:
    all_symptoms.extend(symptom_list)
    
for action_list in df_task1_cleaned['REPAIR_ACTIONS']:
    all_actions.extend(action_list)

symptom_counts = Counter(all_symptoms)
action_counts = Counter(all_actions)

print("Generated Tags Summary:")
print(f"\nFailure Symptoms Distribution:")
for symptom, count in symptom_counts.most_common():
    print(f"  {symptom}: {count}")
    
print(f"\nRepair Actions Distribution:")
for action, count in action_counts.most_common():
    print(f"  {action}: {count}")

print(f"\nComponent Categories:")
component_dist = df_task1_cleaned['COMPONENT_CATEGORY'].value_counts()
for category, count in component_dist.items():
    print(f"  {category}: {count}")

# Convert lists to strings for CSV export
df_task1_cleaned['FAILURE_SYMPTOMS_STR'] = df_task1_cleaned['FAILURE_SYMPTOMS'].apply(lambda x: ', '.join(x))
df_task1_cleaned['REPAIR_ACTIONS_STR'] = df_task1_cleaned['REPAIR_ACTIONS'].apply(lambda x: ', '.join(x))

print(f"\n Tags generated successfully from free text fields")