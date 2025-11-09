import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load the Task 1 dataset (SA-Data-for-Task-1.xlsx)
print("=== LOADING TASK 1 DATASET ===")
try:
    # Load the steering wheel defect data
    df_task1 = pd.read_excel('data/raw/SA-Data-for-Task-1.xlsx', sheet_name='Sheet1')
    print(f" Task 1 data loaded successfully")
    print(f"Dataset shape: {df_task1.shape}")
    print(f"Columns: {list(df_task1.columns)}")
    print("\nFirst few rows:")
    print(df_task1.head(2))
    print("\nColumn data types:")
    print(df_task1.dtypes)
    print("\nMissing values:")
    print(df_task1.isnull().sum())
    
except Exception as e:
    print(f"Error loading Task 1 data: {e}")
    df_task1 = None