import pandas as pd
import numpy as np

def load_and_clean_data(file_path):
    """
    Load and clean the cancer care expenditure data.
    """
    # Read the CSV file with the correct separator
    print(f"Loading data from {file_path}...")
    # First read a few lines to inspect the content
    with open(file_path, 'r') as f:
        first_lines = [next(f) for _ in range(5)]
        print("\nFirst few lines of the file:")
        for line in first_lines:
            print(line.strip())
            
    # Skip the first 3 lines as they are header information
    df = pd.read_csv(file_path, skiprows=3)

    df.drop(columns=['Annual Cost Increase (applied to initial and last phases)'], inplace=True)
    df.drop_duplicates(inplace=True)
    df = df[df['Cancer Site'] != "AllSites"]
    
    print("\nOriginal column names:")
    for col in df.columns:
        print(f"'{col}'")
    
    # Rename columns to be more readable
    column_mapping = {
        'Cancer Site': 'cancer_site',
        'Year': 'year',
        'Sex': 'sex',
        'Age': 'age',
        'Incidence and Survival Assumptions': 'scenario',
        'Annual Cost Increase (applied to initial and last phases)': 'annual_cost_increase',
        'Total Costs': 'total_costs',
        'Initial Year After Diagnosis Cost': 'initial_cost',
        'Continuing Phase Cost': 'continuing_cost',
        'Last Year of Life Cost': 'last_year_cost'
    }
    
    print("\nAttempting to rename columns...")
    df = df.rename(columns=column_mapping)
    
    print("\nColumn names after rename:")
    for col in df.columns:
        print(f"'{col}'")
    
    # Clean numeric columns - remove commas and convert to float
    numeric_columns = ['annual_cost_increase', 'total_costs', 'initial_cost', 
                      'continuing_cost', 'last_year_cost']
    
    for col in numeric_columns:
        if col in df.columns:
            # Remove % sign and commas, then convert to float
            df[col] = df[col].astype(str).str.replace('%', '').str.replace(',', '').astype(float)
        else:
            print(f"\nWarning: Column '{col}' not found in DataFrame!")
    
    # Create scenario categories
    scenario_mapping = {
        'Incidence, Survival at constant rate': 'base_case',
        'Incidence follows recent trend, Survival constant': 'trend_incidence',
        'Survival follows recent trend, Incidence constant': 'trend_survival',
        'Incidence, Survival follow recent trends': 'trend_both'
    }
    df['scenario'] = df['scenario'].map(scenario_mapping)
    
    # Create binary indicators for assumptions
    df['is_trend_incidence'] = df['scenario'].isin(['trend_incidence', 'trend_both'])
    df['is_trend_survival'] = df['scenario'].isin(['trend_survival', 'trend_both'])


    return df

def calculate_derived_features(df):
    """
    Calculate additional features that might be useful for modeling.
    """
    print("Calculating derived features...")
    df = df.copy()
    
    # Calculate cost ratios
    df['continuing_to_initial_ratio'] = df['continuing_cost'] / df['initial_cost']
    df['last_year_to_initial_ratio'] = df['last_year_cost'] / df['initial_cost']
    
    # Calculate percentage of total cost by phase
    df['initial_cost_pct'] = df['initial_cost'] / df['total_costs'] * 100
    df['continuing_cost_pct'] = df['continuing_cost'] / df['total_costs'] * 100
    df['last_year_cost_pct'] = df['last_year_cost'] / df['total_costs'] * 100
    
    return df

def prepare_modeling_data(df):
    """
    Prepare final dataset for modeling.
    """
    print("Preparing final modeling dataset...")
    # Create dummy variables for categorical columns
    categorical_columns = ['cancer_site', 'sex', 'age', 'scenario']
    df_encoded = pd.get_dummies(df, columns=categorical_columns)
    return df_encoded

# Execute the processing pipeline
print("Starting data processing...")
processed_data = load_and_clean_data('expenditure_for_cancer_care.csv')
processed_data = calculate_derived_features(processed_data)

# Save the processed data
output_file = "processed_cancer_care_data.csv"
print(f"Saving processed data to {output_file}...")
processed_data.to_csv(output_file, index=False)


print("Processing complete! Check processed_cancer_care_data.csv for the results.")
print(f"Processed dataset shape: {processed_data.shape}")
