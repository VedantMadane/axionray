
"""
AxionRay Data Analytics Assignment - Complete Analysis Pipeline
Author: Vedant Madane  
Tasks: Data Validation, Integration, and Exploratory Data Analysis
File: Complete implementation using the Excel files
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# ===============================================================================
# DATA LOADING - ACTUAL EXCEL FILES
# ===============================================================================

def load_task1_data():
    """Load Task 1 steering wheel defect data from Excel"""
    print("Loading Task 1 Data: SA-Data-for-Task-1.xlsx")
    try:
        df = pd.read_excel('data/raw/SA-Data-for-Task-1.xlsx', sheet_name='Sheet1')
        print(f" Successfully loaded {df.shape[0]} records with {df.shape[1]} columns")
        return df
    except Exception as e:
        print(f"   Error loading Task 1 data: {e}")
        return None

def load_task2_data():
    """Load Task 2 work order and repair data from Excel"""
    print("Loading Task 2 Data: SA-Data-for-Task-2.xlsx")
    try:
        # Load Work Order Data
        df_wo = pd.read_excel('data/raw/SA-Data-for-Task-2.xlsx', sheet_name='Work Order Data')
        print(f" Work Order Data: {df_wo.shape[0]} records with {df_wo.shape[1]} columns")
        
        # Load Repair Data
        df_rd = pd.read_excel('data/raw/SA-Data-for-Task-2.xlsx', sheet_name='Repair Data') 
        print(f" Repair Data: {df_rd.shape[0]} records with {df_rd.shape[1]} columns")
        
        return df_wo, df_rd
    except Exception as e:
        print(f"   Error loading Task 2 data: {e}")
        return None, None

# ===============================================================================
# TASK 1: DATA VALIDATION AND CLEANING
# ===============================================================================

def analyze_columns(df):
    """Perform comprehensive column-wise analysis"""
    print("\n" + "="*80)
    print("TASK 1: COLUMN-WISE ANALYSIS")
    print("="*80)
    
    # Critical columns for business analysis
    critical_columns = {
        'CAUSAL_PART_NM': 'Root cause component - critical for failure analysis',
        'TOTALCOST': 'Financial impact - critical for cost management', 
        'CUSTOMER_VERBATIM': 'Customer complaint - critical for user experience',
        'REPAIR_AGE': 'Vehicle age at repair - warranty analysis',
        'CORRECTION_VERBATIM': 'Repair action - operational insights'
    }
    
    print("Top 5 Critical Columns:")
    for i, (col, desc) in enumerate(critical_columns.items(), 1):
        print(f"{i}. {col}: {desc}")
    
    # Detailed analysis
    print("\nDetailed Analysis:")
    for col in critical_columns.keys():
        if col in df.columns:
            print(f"\n{col}:")
            print(f"  Data type: {df[col].dtype}")
            print(f"  Unique values: {df[col].nunique()}")
            print(f"  Missing values: {df[col].isnull().sum()}")
            if df[col].dtype in ['int64', 'float64']:
                print(f"  Range: {df[col].min():.2f} - {df[col].max():.2f}")
    
    return critical_columns

def clean_task1_data(df):
    """Clean and prepare Task 1 data"""
    print("\n" + "="*80)
    print("TASK 1: DATA CLEANING")
    print("="*80)
    
    df_clean = df.copy()
    
    # Handle missing values
    print("Handling missing values...")
    missing_before = df_clean.isnull().sum().sum()
    
    # Fill missing values with appropriate defaults
    df_clean['CAUSAL_PART_NM'] = df_clean['CAUSAL_PART_NM'].fillna('UNKNOWN')
    df_clean['PLANT'] = df_clean['PLANT'].fillna('UNKNOWN')  
    df_clean['STATE'] = df_clean['STATE'].fillna('UNKNOWN')
    
    # Text standardization
    df_clean['CUSTOMER_VERBATIM_CLEAN'] = df_clean['CUSTOMER_VERBATIM'].str.upper().str.strip()
    df_clean['CORRECTION_VERBATIM_CLEAN'] = df_clean['CORRECTION_VERBATIM'].str.upper().str.strip()
    
    # Create derived categories
    def categorize_cost_severity(cost):
        if cost < 100: return 'LOW'
        elif cost < 500: return 'MEDIUM' 
        elif cost < 1500: return 'HIGH'
        else: return 'CRITICAL'
    
    df_clean['COST_SEVERITY'] = df_clean['TOTALCOST'].apply(categorize_cost_severity)
    
    def categorize_warranty(age):
        if age <= 1: return 'NEW_VEHICLE'
        elif age <= 3: return 'BASIC_WARRANTY'
        elif age <= 5: return 'EXTENDED_WARRANTY'
        else: return 'OUT_OF_WARRANTY'
    
    df_clean['WARRANTY_STATUS'] = df_clean['REPAIR_AGE'].apply(categorize_warranty)
    
    missing_after = df_clean.isnull().sum().sum()
    print(f" Missing values reduced: {missing_before} → {missing_after}")
    print(f" Created cost severity and warranty categories")
    
    return df_clean

def generate_text_tags(df):
    """Generate meaningful tags from free text fields"""
    print("\n" + "="*80)
    print("TASK 1: TEXT TAG GENERATION")
    print("="*80)
    
    def extract_failure_symptoms(text):
        if pd.isna(text):
            return ['UNKNOWN']
            
        text_upper = str(text).upper()
        symptoms = []
        
        # Material degradation symptoms
        if any(word in text_upper for word in ['COMING APART', 'COMING OFF', 'PEELING', 'STITCHING', 'TEAR', 'RIP', 'FRAY']):
            symptoms.append('MATERIAL_DEGRADATION')
            
        # Functional failure symptoms  
        if any(word in text_upper for word in ['NOT WORK', 'INOP', 'INOPERATIVE', 'FAILS', 'BROKEN', 'MALFUNCTION', "WON'T", 'WONT']):
            symptoms.append('FUNCTIONAL_FAILURE')
            
        # Noise issues
        if any(word in text_upper for word in ['NOISE', 'RUBBING', 'CLICKING', 'SOUND', 'SQUEAK', 'RATTLE']):
            symptoms.append('NOISE_ISSUE')
            
        # Temperature regulation issues
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
    
    def extract_repair_actions(text):
        if pd.isna(text): return ['UNKNOWN']
        text = str(text).upper()
        actions = []
        
        if 'REPLACED' in text: actions.append('REPLACEMENT')
        if 'ADJUSTED' in text: actions.append('ADJUSTMENT')
        if 'REPAIRED' in text: actions.append('REPAIR')
        if 'PROGRAMMED' in text: actions.append('SOFTWARE_UPDATE')
        if 'DIAGNOSED' in text: actions.append('DIAGNOSTIC')
        
        return actions if actions else ['OTHER']
    
    # Apply tag extraction
    df['FAILURE_SYMPTOMS'] = df['CUSTOMER_VERBATIM'].apply(extract_failure_symptoms)
    df['REPAIR_ACTIONS'] = df['CORRECTION_VERBATIM'].apply(extract_repair_actions)
    
    # Count tag frequencies
    all_symptoms = [s for symptoms in df['FAILURE_SYMPTOMS'] for s in symptoms]
    all_actions = [a for actions in df['REPAIR_ACTIONS'] for a in actions]
    
    symptom_counts = Counter(all_symptoms)
    action_counts = Counter(all_actions)
    
    print("Generated Tags:")
    print("\nFailure Symptoms:")
    for symptom, count in symptom_counts.most_common():
        print(f"  {symptom}: {count}")
    
    print("\nRepair Actions:")
    for action, count in action_counts.most_common():
        print(f"  {action}: {count}")
    
    # Convert to strings for CSV export
    df['FAILURE_SYMPTOMS_STR'] = df['FAILURE_SYMPTOMS'].apply(lambda x: ', '.join(x))
    df['REPAIR_ACTIONS_STR'] = df['REPAIR_ACTIONS'].apply(lambda x: ', '.join(x))
    
    return df, symptom_counts, action_counts

# ===============================================================================
# TASK 2: DATA INTEGRATION
# ===============================================================================

def analyze_primary_keys(df_wo, df_rd):
    """Analyze and select primary key for integration"""
    print("\n" + "="*80)
    print("TASK 2: PRIMARY KEY ANALYSIS")
    print("="*80)
    
    wo_keys = set(df_wo['Primary Key'])
    rd_keys = set(df_rd['Primary Key'])
    common_keys = wo_keys.intersection(rd_keys)
    
    print(f"Work Orders unique keys: {len(wo_keys)}")
    print(f"Repair Data unique keys: {len(rd_keys)}")
    print(f"Common keys: {len(common_keys)}")
    print(f"Work Orders only: {len(wo_keys - rd_keys)}")
    print(f"Repair Data only: {len(rd_keys - wo_keys)}")
    
    print("\n Selected Primary Key: 'Primary Key'")
    print("Justification:")
    print("• Explicitly named as Primary Key in both datasets")
    print("• Unique format: SO[ORDER]-[SEGMENT] ensures uniqueness")  
    print(f"• {len(common_keys)} matching records for reliable integration")
    
    return common_keys

def clean_task2_data(df_wo, df_rd):
    """Clean Task 2 datasets for integration"""
    print("\n" + "="*80)
    print("TASK 2: DATA CLEANING")
    print("="*80)
    
    # Clean Work Orders
    df_wo_clean = df_wo.copy()
    df_wo_clean['Order Date'] = pd.to_datetime(df_wo_clean['Order Date'])
    df_wo_clean['Cause'] = df_wo_clean['Cause'].fillna('Not Specified')
    df_wo_clean['Correction'] = df_wo_clean['Correction'].fillna('No details provided')
    
    # Clean Repair Data  
    df_rd_clean = df_rd.copy()
    
    def clean_currency(value):
        if pd.isna(value): return 0.0
        if isinstance(value, str):
            return float(value.replace('$', '').replace(',', ''))
        return float(value)
    
    df_rd_clean['Cost_Numeric'] = df_rd_clean['Cost'].apply(clean_currency)
    df_rd_clean['Coverage'] = df_rd_clean['Coverage'].fillna('Not Specified')
    df_rd_clean['Actual Hours'] = df_rd_clean['Actual Hours'].fillna(0.0)
    
    print(" Work Order Data cleaned")
    print(" Repair Data cleaned and costs converted to numeric")
    
    return df_wo_clean, df_rd_clean

def integrate_datasets(df_wo_clean, df_rd_clean):
    """Merge datasets using inner join"""
    print("\n" + "="*80)
    print("TASK 2: DATA INTEGRATION")
    print("="*80)
    
    print("Join Strategy: INNER JOIN")
    print("Rationale:")
    print("• Ensures complete records with both work orders and repair costs")
    print("• Eliminates incomplete records that could skew analysis")
    print("• Provides reliable dataset for trend analysis")
    
    df_merged = pd.merge(df_wo_clean, df_rd_clean, on='Primary Key', how='inner', suffixes=('_WO', '_RD'))
    
    # Add derived columns
    df_merged['Cost_Per_Hour'] = df_merged['Cost_Numeric'] / (df_merged['Actual Hours'] + 0.1)
    df_merged['Year'] = df_merged['Order Date'].dt.year
    
    print(f" Integration successful: {df_merged.shape[0]} records merged")
    print(f"Date range: {df_merged['Order Date'].min()} to {df_merged['Order Date'].max()}")
    
    return df_merged

# ===============================================================================
# TASK 3: EXPLORATORY DATA ANALYSIS
# ===============================================================================

def perform_trend_analysis(df_merged):
    """Comprehensive trend analysis"""
    print("\n" + "="*80)
    print("TASK 3: TREND ANALYSIS")
    print("="*80)
    
    # Cost-Hours correlation
    df_analysis = df_merged[(df_merged['Actual Hours'] > 0) & (df_merged['Cost_Numeric'] > -1000)]
    correlation = df_analysis['Cost_Numeric'].corr(df_analysis['Actual Hours'])
    print(f"Cost vs Hours Correlation: {correlation:.3f}")
    
    # Yearly trends
    yearly = df_merged.groupby('Year').agg({
        'Cost_Numeric': ['sum', 'mean', 'count'],
        'Actual Hours': ['sum', 'mean']
    }).round(2)
    print("\nYearly Trends:")
    print(yearly)
    
    # Category analysis
    category = df_merged.groupby('Product Category').agg({
        'Cost_Numeric': ['mean', 'sum', 'count'],
        'Actual Hours': 'mean'
    }).round(2)
    print("\nProduct Category Analysis:")
    print(category)
    
    return correlation, yearly, category

def identify_root_causes(df_merged):
    """Identify failure patterns and root causes"""
    print("\n" + "="*80)
    print("TASK 3: ROOT CAUSE ANALYSIS")
    print("="*80)
    
    # Extract components from failure conditions
    def extract_component(failure_condition):
        if pd.isna(failure_condition): return 'Unknown'
        parts = str(failure_condition).split(' - ')
        return parts[1].strip() if len(parts) > 1 else 'Not Mentioned'
    
    df_merged['Failed_Component'] = df_merged['Failure Condition - Failure Component'].apply(extract_component)
    
    # Component failure analysis
    component_failures = df_merged['Failed_Component'].value_counts()
    print("Top Failed Components:")
    for component, count in component_failures.head(8).items():
        print(f"  {component}: {count}")
    
    # Cost impact by component
    component_costs = df_merged.groupby('Failed_Component').agg({
        'Cost_Numeric': ['mean', 'sum', 'count'],
        'Actual Hours': 'mean'
    }).round(2)
    
    print("\nCost Impact by Component:")
    print(component_costs.head(8))
    
    return component_failures, component_costs

# ===============================================================================
# MAIN EXECUTION PIPELINE
# ===============================================================================

def main():
    """Execute complete AxionRay analysis pipeline"""
    print("AxionRay Data Analytics Assignment - Complete Analysis")
    print("="*80)
    
    # Load data
    df_task1 = load_task1_data()
    df_wo, df_rd = load_task2_data()
    
    if df_task1 is None or df_wo is None or df_rd is None:
        print("   Failed to load required data files")
        return
    
    # Task 1: Data Validation
    critical_cols = analyze_columns(df_task1)
    df_task1_clean = clean_task1_data(df_task1)
    df_task1_tagged, symptoms, actions = generate_text_tags(df_task1_clean)
    
    # Save Task 1 results
    task1_export_cols = [
        'VIN', 'TRANSACTION_ID', 'REPAIR_DATE', 'CUSTOMER_VERBATIM', 'CORRECTION_VERBATIM',
        'CAUSAL_PART_NM', 'TOTALCOST', 'REPAIR_AGE', 'COST_SEVERITY', 'WARRANTY_STATUS',
        'FAILURE_SYMPTOMS_STR', 'REPAIR_ACTIONS_STR'
    ]
    df_task1_final = df_task1_tagged[task1_export_cols]
    df_task1_final.to_csv('data/processed/task1_cleaned_tagged_data.csv', index=False)
    print("\n Task 1 completed: task1_cleaned_tagged_data.csv saved")
    
    # Task 2: Data Integration
    common_keys = analyze_primary_keys(df_wo, df_rd)
    df_wo_clean, df_rd_clean = clean_task2_data(df_wo, df_rd)
    df_merged = integrate_datasets(df_wo_clean, df_rd_clean)
    
    # Save Task 2 results
    task2_export_cols = [
        'Primary Key', 'Order Date', 'Manufacturer', 'Product Category', 'Complaint',
        'Part Description', 'Cost_Numeric', 'Actual Hours', 'Year'
    ]
    df_task2_final = df_merged[task2_export_cols]
    df_task2_final.to_csv('data/processed/task2_integrated_data.csv', index=False)
    print("\n Task 2 completed: task2_integrated_data.csv saved")
    
    # Task 3: Exploratory Data Analysis
    correlation, yearly, category = perform_trend_analysis(df_merged)
    failures, costs = identify_root_causes(df_merged)
    
    # Save Task 3 results with analysis summary
    summary = {
        'total_records': len(df_merged),
        'cost_hours_correlation': correlation,
        'total_cost': df_merged['Cost_Numeric'].sum(),
        'total_revenue': df_merged['Revenue'].sum(),
        'top_failure': failures.index[0] if len(failures) > 0 else 'Unknown'
    }
    
    summary_df = pd.DataFrame([summary])
    summary_df.to_csv('data/processed/task3_analysis_summary.csv', index=False)
    print("\n Task 3 completed: task3_analysis_summary.csv saved")
    
    print("\n" + "="*80)
    print("  AXIONRAY ANALYSIS COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("Generated Files:")
    print("• task1_cleaned_tagged_data.csv - Cleaned steering defect data with tags")
    print("• task2_integrated_data.csv - Merged work order and repair data") 
    print("• task3_analysis_summary.csv - EDA results and key insights")
    print("\nKey Insights:")
    print(f"• {len(df_task1)} steering defect records analyzed")
    print(f"• {len(df_merged)} integrated repair records")
    print(f"• Cost-Hours correlation: {correlation:.3f}")

if __name__ == "__main__":
    main()
