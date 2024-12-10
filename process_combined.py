import pandas as pd 
import numpy as np

data = pd.read_csv("combined.csv")

df = pd.DataFrame(data)

# mapping old column names to new readable ones
column_name_mapping = {
    'REGION22': 'Region',
    'FAMS1231': 'Family Size',
    'RXEXP22': 'Prescription Cost Spent',
    'CANCERDX': 'Cancer Diagnosis',
    'UNINS22': 'Uninsured',
    'PRVEV22': 'Private Insurance',
    'MCDEV22': 'Medicaid Status',
    'MCREV22': 'Medicare Status',
    'HOUR53': 'Hours Worked',
    'EMPST53': 'Employment Status',
    'FAMINC22': 'Family Income',
    'HIDEG': 'Highest Degree',
    'MARRY22X': 'Marital Status',
    'RACEV1X': 'Race',
    'SEX': 'Sex',
    'AGELAST': 'Age',
    'TOTSLF22': 'Out of Pocket Cost',
    'CABLADDR': 'Bladder Cancer',
    'CABREAST': 'Breast Cancer',
    'CACERVIX': 'Cervix Cancer',
    'CACOLON': 'Colon Cancer',
    'CALUNG': 'Lung Cancer',
    'CALYMPH': 'Lymphoma Cancer',
    'CAMELANO': 'Melanoma Cancer',
    'CAOTHER': 'Other Cancer',
    'CAPROSTA': 'Prostate Cancer',
    'CASKINNM': 'Skin Nonmelanoma Cancer',
    'CASKINDK': 'Skin Unknown Cancer',
    'CAUTERUS': 'Uterus Cancer'
}

# Rename the columns in the DataFrame
df.rename(columns=column_name_mapping, inplace=True)

print(df.columns)



df['Total Cancer Types'] = df[['Bladder Cancer', 'Breast Cancer', 'Cervix Cancer', 
                              'Colon Cancer', 'Lung Cancer', 'Lymphoma Cancer',
                              'Melanoma Cancer', 'Other Cancer', 'Prostate Cancer',
                              'Skin Nonmelanoma Cancer', 'Skin Unknown Cancer', 
                              'Uterus Cancer']].sum(axis=1)

df['Has Multiple Cancers'] = (df['Total Cancer Types'] > 1).astype(int)

df['Cost per Family Member'] = df['Out of Pocket Cost'] / df['Family Size']

df['Senior'] = (df['Age'] >= 65).astype(int)
df['Working Age'] = ((df['Age'] >= 18) & (df['Age'] < 65)).astype(int)

df['Income per Capita'] = df['Family Income'] / df['Family Size']
df['High Income'] = (df['Income per Capita'] > df['Income per Capita'].median()).astype(int)

df['Full Time'] = (df['Hours Worked'] >= 40).astype(int)
df['Part Time'] = ((df['Hours Worked'] < 40) & (df['Hours Worked'] > 0)).astype(int)

df['Higher Education'] = df['Highest Degree'].isin(['BACHELOR\'S DEGREE', 'MASTER\'S DEGREE', 
                                                   'DOCTORATE DEGREE']).astype(int)

df['High Prescription Cost'] = (df['Prescription Cost Spent'] > df['Prescription Cost Spent'].median()).astype(int)

df['Female Specific Cancer'] = ((df['Breast Cancer'] == 1) | 
                              (df['Cervix Cancer'] == 1) |
                              (df['Uterus Cancer'] == 1)).astype(int)

df['Male Specific Cancer'] = (df['Prostate Cancer'] == 1).astype(int)


print(df.columns)

df.to_csv('processed_combined.csv')