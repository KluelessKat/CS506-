import pandas as pd
import numpy as np


cancer_name_map = {
    'bladder_cancer': 'CABLADDR',
    'breast_cancer': 'CABREAST',
    'cervix_cancer': 'CACERVIX',
    'colon_cancer': 'CACOLON',
    'lung_cancer': 'CALUNG',
    'lymphoma_cancer': 'CALYMPH',
    'melanoma_cancer': 'CAMELANO',
    'other_cancer': 'CAOTHER',
    'prostate_cancer': 'CAPROSTA',
    'skin_nonmelanoma_cancer': 'CASKINNM',
    'skin_unknown_cancer': 'CASKINDK',
    'uterus_cancer': 'CAUTERUS'
}

highest_degrees = ["No Degree", "GED", "High School", "Bachelor's", "Master's", "Doctorate", "Other", "Underage"]

race_mapping = {
    1: 'white',
    2: 'black',
    3: 'amer_indian_alaska_native',
    4: 'asian_native_hawaiian_pacific_isl',
    6: 'multiple_races_reported'
}

region_map = {
  1: 'Northeast',
  2: 'Midwest',
  3: 'South',
  4: 'West'
}

gender_map = {
    1: 'male',
    2: 'female'
}

def reverse_map(input_dict):
    """
    Reverses the keys and values of a given dictionary.

    Parameters:
    input_dict (dict): The dictionary to reverse.

    Returns:
    dict: A new dictionary with the keys and values swapped.
    """
    return {v: k for k, v in input_dict.items()}


def generate_plotting_data(dataset_path, cancer_type):
    """
    Convert the dataset into plotting data based on the specified features.

    Parameters:
        dataset_path (str): Path to the CSV dataset.

    Returns:
        pd.DataFrame: Aggregated data for plotting.
    """
    # Load the dataset
    df = pd.read_csv(dataset_path)

    df = df[df['cancer_type'] == cancer_name_map[cancer_type]]


    # Plot 1
    plt_data = dict()


    age_avg = df.groupby('age')['insurance_cover'].mean().reset_index()
    
    # Convert the result to a dictionary of lists
    plt_data['age'] = {
        'age': age_avg['age'].tolist(),
        'insurance_cover': age_avg['insurance_cover'].tolist()
    }

    # Filter the DataFrame based on the highest degree column and then calculate the average insurance cover for each degree
    degree_mask = (df['highest_degree'] >= 1.0)

    highest_degree = df.loc[degree_mask, ['highest_degree', 'insurance_cover']]
    
    # Mapping the 'highest_degree' values to their corresponding labels from `features`
    highest_degree['highest_degree'] = highest_degree['highest_degree'].map(lambda x: highest_degrees[int(x) - 1])
    
    # Group by the 'highest_degree' and calculate the average insurance_cover
    highest_degree_avg = highest_degree.groupby('highest_degree')['insurance_cover'].mean().reset_index()
    
    # Convert the result to a dictionary of lists
    highest_degree_dict = {
        'highest_degree': highest_degree_avg['highest_degree'].tolist(),
        'insurance_cover': highest_degree_avg['insurance_cover'].tolist()
    }
    
    plt_data['highest_degree'] = highest_degree_dict

    def categorize_employment_status(status):
      if status in [1.0, 2.0, 3.0]:  # employed
          return 'employed'
      elif status == 0.0:  # not employed
          return 'not_employed'
      else:  # other
          return 'other'

    df['employment_category'] = df['employment_status'].apply(categorize_employment_status)
    result = df.groupby(['employment_category', 'insurance_type'])['insurance_cover'].mean().unstack(fill_value=0)
    plt_data['employment_statuses'] = result.to_dict(orient='index')

    df['family_size'] = df['family_size'].fillna(-1)
    average_insurance_cover = df.groupby('family_size')['insurance_cover'].mean()

    average_insurance_cover = {
      "family_size": average_insurance_cover.index.tolist(),
      "amount": average_insurance_cover.tolist()
    }
    plt_data['family_size'] = average_insurance_cover



    income_bins = [0, 30000, 60000, 100000, float("inf")]
    income_labels = ["<30k", "30k-60k", "60k-100k", "100k+"]
    out_of_pocket_bins = [0, 5000, 10000, 15000, 20000, float("inf")]
    out_of_pocket_labels = ["0-5k", "5k-10k", "10k-15k", "15k-20k", "20k+"]
    
    # Bin the data
    df['income_bin'] = pd.cut(df['family_income'], bins=income_bins, labels=income_labels, right=False)
    df['out_of_pocket_bin'] = pd.cut(df['out_of_pocket'], bins=out_of_pocket_bins, labels=out_of_pocket_labels, right=False)
    
    # Create the dictionary for family_income and out_of_pocket
    plt_data['family_income'] =  df['out_of_pocket_bin'].value_counts().to_dict()
    plt_data['family_income'].update(df['income_bin'].value_counts().to_dict())

    df['race_name'] = df['race'].map(race_mapping)
    result = df.groupby(['race_name', 'insurance_type'])['insurance_cover'].mean().unstack(fill_value=0)
    plt_data['race'] = result.to_dict(orient='index')


    df2 = df[df['region'] > 0]
    df2['region_name'] = df2['region'].map(region_map)
    result = df2.groupby(['region_name', 'insurance_type'])['insurance_cover'].mean().unstack(fill_value=0)
    region_dict = result.to_dict(orient='index')

    plt_data['region'] = region_dict
   
    return plt_data

# Example usage
if __name__ == "__main__":
    dataset_path = "data/processed/results.csv"
    plotting_data = generate_plotting_data(dataset_path, "bladder_cancer")
    print(plotting_data)

