import pandas as pd
import numpy as np

df = pd.read_stata('processed_h243.dta')

# Prescription cost metrics
df['Prescription_Cost_Burden'] = df['Prescription_Cost_Spent'] / df['Family_Size']

# Age-based features
df['Senior'] = (df['Age'] >= 65).astype(int)
df['Working_Age'] = ((df['Age'] >= 18) & (df['Age'] < 65)).astype(int)

# Income metrics
df['Income_per_Capita'] = df['Family_Income'] / df['Family_Size']
df['High_Income'] = (df['Income_per_Capita'] > df['Income_per_Capita'].median()).astype(int)

# Employment intensity
df['Full_Time'] = (df['Hours_Worked'] >= 40).astype(int)
df['Part_Time'] = ((df['Hours_Worked'] < 40) & (df['Hours_Worked'] > 0)).astype(int)

df.to_stata('enhanced_h243.dta')