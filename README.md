# **CS 506 Final Project: Predicting Financial Toxicity for Cancer Patients**

## **Table of Contents**

1. Project Overview

2. Motivation

3. Data Acquisition, Processing, and Cleaning

4. Visualization and Exploratory Data Analysis

5. Data Modeling

6. Results

7. Conclusion

8. How to Build and Run the Code

9. References

***


## **Project Overview**

This project aims to predict financial toxicity for cancer patients by analyzing and modeling the relationship between various socio-economic, demographic, and health-related variables. Financial toxicity is measured as the ratio of out-of-pocket expenses to household income, and our goal is to identify patterns or biases in treatment costs based on insurance coverage, region, race, and other factors.

Our tool incorporates data visualization, interactive exploratory data analysis (EDA), and machine learning prediction models into a web-based application. Users can explore data trends and predict financial toxicity based on their inputs.

***


## **Motivation**

The rising cost of cancer care, coupled with the significant financial burden it imposes, remains a pressing concern, especially for those in vulnerable demographics or regions. Our preliminary analysis of historical cancer cost trends revealed:

1. A steady increase in treatment costs over time, highlighting the growing financial burden on patients.

2. Minimal variation in costs based on cancer stage, suggesting that the rising costs are largely independent of the progression of the disease.

![image1](https://github.com/user-attachments/assets/965097f9-ba16-4b5c-a13b-94a043ed6d91)

These findings led us to pivot our focus towards understanding **who bears the brunt of these increasing costs**, rather than just quantifying the costs themselves. By examining demographic biases and disparities in insurance coverage and out-of-pocket costs, we hope to provide a clearer picture of the factors contributing to financial toxicity and offer insights into reducing this burden.

This project seeks to:

1. Identify biases in insurance coverage and treatment costs.

2. Explore if certain demographic groups are at greater risk of financial toxicity.

3. Provide actionable insights for policymakers and healthcare providers to reduce disparities in cancer care and ensure that resources are allocated effectively to support those in need.

4. Enable patients to better understand their financial risk and make informed decisions with our predictive tools.

***


## **Data Acquisition, Processing, and Cleaning**

### **Acquisition and Source**

The dataset was acquired from the MEPS (Medical Expenditure Panel Survey) full-year consolidated data for 2020, 2021, and 2022.


### **Data Overview**

Data processing is a crucial component of this project, ensuring that the datasets from the Medical Expenditure Panel Survey (MEPS) are cleaned, harmonized, and made ready for analysis and modeling. Our analysis specifically leverages the following variables:

1. **Demographics:** Region, age, race, gender, marital status, education level.

2. **Socio-economic factors:** Family income, family size, hours worked, employment status.

3. **Insurance coverage:** Medicare, Medicaid, private insurance, uninsured status, Veteran's Administration, Tricare.

4. **Cancer-specific variables:** Cancer diagnosis, types of cancer (lung, breast, prostate, etc.).

5. **Financial metrics:** Out-of-pocket expenses, prescription costs, and total expenditures paid by various insurance types.


### **Data Cleaning and Processing**

#### **1. Initialization and Data Loading**

We iteratively load each dataset using the `pandas` library, maintaining a single unified DataFrame (`data`). Each year's dataset is processed to:

- Extract patient identifiers (`DUPERSID`) as unique identifiers.

- Map year-dependent variables (e.g., `TOTMCD22` for Medicaid coverage in 2022) to common column names.


#### **2. Mapping Variables**

- **Constant Variables:** Some variables remain consistent across all datasets (e.g., age, race, education). These are directly mapped to their corresponding columns in the unified dataset.

- **Year-Dependent Variables:** Variables such as insurance coverage and regional identifiers differ by year (e.g., `MCDEV22` for Medicaid in 2022). These are processed dynamically by appending the year suffix and mapped to a standard column (e.g., `insurance_cover`).


#### **3. Handling Categorical Variables**

Categorical variables such as race, marital status, and education are processed to ensure consistency. For example:

- Race (`RACEV1X`) is encoded into categories such as "White," "Black," "Asian," and "Multiple Races."

- Education (`HIDEG`) is categorized into "High School," "Bachelor's," "Master's," etc., with special codes (e.g., -8, -7) treated as missing or inapplicable data.

- Insurance types are binary-encoded (e.g., "1 YES" for coverage, "0 NO" for lack of coverage).


#### **4. Cancer-Specific Variables**

Cancer type variables (e.g., `CALUNG` for lung cancer, `CABREAST` for breast cancer) are processed to indicate the presence or absence of each cancer type. Patients diagnosed with any cancer (`CANCERDX = 1`) are included in the final dataset, and their cancer types are consolidated into a single `cancer_type` column.


#### **5. Cleaning and Transforming Financial Data**

Financial data, including out-of-pocket expenses (`TOTSLF22`), prescription costs (`RXEXP22`), and insurance contributions (`TOTMCD22`, `TOTPRV22`), are cleaned and standardized:

- Negative or invalid values are treated as missing data.

- Contributions by different payers (e.g., Medicaid, Medicare, private insurance) are aggregated to compute total coverage.


#### **6. Data Harmonization Across Years**

To harmonize the datasets across years:

- Common variables are aligned across datasets with consistent naming conventions.

- Year-specific suffixes are removed to ensure unified column names (e.g., `REGION22` becomes `region`).

- Data from each year is appended to the unified DataFrame, ensuring consistency in variable representations.


#### **7. Filtering and Deduplication**

The dataset is filtered to include only patients diagnosed with cancer (`CANCERDX = 1`). Duplicate records are removed based on the unique identifier (`DUPERSID`).


#### **8. Output**

The final cleaned dataset is exported as a CSV file (`results.csv`) for downstream analysis and modeling. Key features include demographic details, insurance coverage types, cancer types, and financial metrics, all harmonized across the three years of MEPS data.

***


## **Visualization and Exploratory Data Analysis**

### **Exploratory Data Analysis**

Interactive plots are integrated into our web app. Key EDA plots we used to extract insights include:


**1. Amount vs Age:** This graph shows that age does not significantly impact cancer treatment costs. The lack of correlation indicates that other variables, such as insurance type or income, are likely more influential in determining financial burden.

**2. Amount vs Highest Degree Obtained:** This graph highlights that individuals with lower educational attainment incur higher treatment costs. It suggests that socio-economic advantages associated with higher education, like better access to private insurance, may reduce financial toxicity.

**3. Coverage vs Employment Status:** This graph emphasizes the dependence of unemployed individuals on public insurance (e.g., Medicaid) and the dominance of private insurance among the employed. It highlights the role of stable employment in reducing financial vulnerability.

**4. Amount vs Family Size:** Family size shows minimal impact on treatment costs, suggesting that cancer-related expenses are primarily individualistic and not influenced by household composition.

**5. Total Out-of-Pocket vs Income:** This graph demonstrates the disproportionate financial burden on lower-income groups. It underscores the need for targeted policies to alleviate financial toxicity for economically disadvantaged households.

**6. Coverage vs Race**: Racial disparities in insurance access are evident, with minority groups relying more on Medicaid and Medicare while white individuals have greater access to private insurance. This reflects systemic healthcare inequities.

**7. Coverage vs Region:** Geographic disparities are clear, with private insurance more prevalent in the Midwest and Medicaid more common in the South. These differences likely stem from regional policies and economic conditions affecting healthcare access.


![image2](https://github.com/user-attachments/assets/c0777ff6-ac67-4e93-bef8-4eb3e5804bbd)


### **Key Observations**

**Bias Indications:**


**1. Coverage vs Race**

The data reveals notable disparities in insurance coverage among different racial groups, with certain types of insurance, particularly private insurance, being more accessible to white individuals compared to minority groups. Minority populations, such as "Asian/Native Hawaiian/Pacific Islander" and those identifying as "Multiple Races Reported," are underrepresented in private insurance coverage and also show lower utilization of programs like Medicare. This disparity suggests the presence of systemic biases and socio-economic barriers that disproportionately affect minority groups. Factors such as employment inequities, regional disparities in healthcare access, and structural barriers to private insurance enrollment may contribute to this gap. The lack of access to private insurance for these groups not only limits their healthcare options but also exacerbates financial vulnerability when facing significant medical expenses, such as those associated with cancer treatment. These findings underscore the importance of addressing racial inequities in insurance access to reduce financial toxicity and promote equitable healthcare outcomes.


**2. Coverage vs Region**

Private insurance is notably more prevalent in the Midwest, suggesting that individuals in this region may have greater access to employer-sponsored insurance plans or higher incomes that allow for private coverage. In contrast, Medicaid and other public insurance programs are more dominant in the South, which may reflect broader socio-economic conditions, such as lower average household incomes or higher rates of unemployment. These regional differences are likely influenced by state-level healthcare policies, including Medicaid expansion decisions under the Affordable Care Act, as well as varying economic conditions that impact employment benefits and healthcare accessibility. Such disparities point to the critical role that geographic location plays in determining insurance type and, by extension, an individual’s financial risk when managing significant healthcare costs. Addressing these regional inequities will require targeted policy interventions that account for both economic and systemic factors driving these differences.


**3. Coverage vs Employment Status**

The data shows a divide in insurance coverage based on employment status, with private insurance being disproportionately higher among employed individuals and Medicaid or other public insurance programs predominantly utilized by those categorized as "other," including unemployed individuals or those in non-standard employment. This pattern aligns with the expectation that private insurance is frequently tied to employment benefits, making it more accessible to individuals with stable jobs. For unemployed individuals or those in non-traditional work arrangements, economic barriers further limit access to private insurance, leaving public insurance as the only viable option.

This divide underscores the structural inequities embedded in the healthcare system, where access to higher-quality or more comprehensive insurance often depends on an individual's employment status. Consequently, those without stable employment may face a dual burden: limited access to private insurance and greater financial toxicity due to reliance on public insurance programs that may have higher out-of-pocket costs or limited coverage for specialized treatments. These findings suggest that systemic reforms, such as decoupling insurance from employment or expanding access to affordable private insurance plans, could help mitigate these inequities and ensure broader healthcare coverage for economically vulnerable populations. Additionally, targeted support programs for unemployed individuals could help bridge this gap, reducing financial toxicity and improving healthcare equity.


**4. Total Out-of-Pocket vs Income**

The data shows that lower-income households (<$30k) face disproportionately high out-of-pocket healthcare expenses, which decline significantly for higher income groups. This highlights severe financial toxicity for low-income populations, suggesting that current insurance systems fail to adequately protect these groups. Targeted interventions, such as cost caps or subsidies, are needed to reduce financial strain and improve healthcare equity.


**5. Amount vs Highest Degree Obtained**

Individuals with lower educational attainment, such as those with a GED or high school diploma, tend to incur higher healthcare costs compared to individuals holding advanced degrees like a Master’s or Doctorate. This disparity is likely influenced by socio-economic factors, as higher levels of education are frequently associated with improved employment prospects and greater access to employer-sponsored private insurance. Consequently, those with limited educational backgrounds may face greater financial barriers to healthcare, further exacerbating disparities in treatment affordability and financial stability.




**Insignificant Differences:**

**6. Amount vs Age**

The data reveals no clear correlation between age and cancer treatment costs, with younger and older age groups showing similar expense distributions. This lack of variation suggests that age is not a primary determinant of cancer-related expenses. Instead, other factors, such as insurance type or the treatment phase, likely play a more significant role in influencing healthcare costs.


**7. Amount vs Family Size**

Lastly, the data indicates that family size has minimal impact on cancer treatment costs, with expenditures remaining concentrated within a narrow range regardless of household size. This suggests that cancer-related expenses are primarily individualistic and are not significantly influenced by the size of the family unit.




## **Data Modeling**

### **Additional Data Processing**

On top of the preprocessing and cleaning we performed on the dataset, we one-hot encoded categorical variables such as insurance type and cancer type. As many values in the expenditure columns are much larger, we normalized these numerical features with StandardScaler() to improve model performance.


### **Modeling Approach**

#### **Model Objective**

To predict out-of-pocket costs for cancer patients using all selected features.


#### **Algorithms Explored**

We empirically tested various models and concluded that ensembles showed the best performance as shown below:

![image3](https://github.com/user-attachments/assets/f456ee11-6ae6-43f9-8ce3-cca86d934c09)

This also makes sense since the ensembles are more robust and better for handling missing values (although we processed our dataset to account for missing values, the flexibility of the model was a strength). We can see that boosting ensembles such as XGBoost perform better than bagging ensembles like RandomForest. In order to narrow down the best boosting ensemble model, we chose to test 3 types of boosting ensembles: 

1. CatBoost Regressor

2. XGBoost Regressor

3. LightGBM Regressor

The models were evaluated using the following metrics:

1. Root Mean Squared Error (RMSE): Measures prediction error.

2. Mean Absolute Error (MAE): Measures absolute differences between actual and predicted values.

3. Custom Accuracy: Percentage of predictions within a 10% tolerance.

**Results:**

- CatBoost: RMSE = 1.73, MAE = 1.31, Custom Accuracy = 33.19%

- XGBoost: RMSE = 1.84, MAE = 1.34, Custom Accuracy = 34.50%

- LightGBM: RMSE = 1.79, MAE = 1.33, Custom Accuracy = 32.53%

![image4](https://github.com/user-attachments/assets/0cf2f3e1-270d-49e4-b223-864e9dd3bee1)

While CatBoost performed slightly better in terms of RMSE, the difference was minimal. Ultimately, LightGBM was selected as the final model due to its faster training time and comparable accuracy. LightGBM was also a good choice because its tree-leaf-based splitting mechanism accelerates training without compromising accuracy.


#### **Model Pipeline**

With the chosen model, we continued to program our financial toxicity predictive tool with the following pipeline.

1. Train/Test Split: Data was split into 70% training and 30% testing sets.

2. Hyperparameter Tuning: Grid search was performed to optimize model parameters.

3. Evaluation: Performance metrics were calculated on both training and test sets.

   1. RMSE: 1.7649

   2. R-squared: 0.3946

***


## **Results**

### **Data Insights**

1. Private insurance provided better coverage across all regions, but disparities exist based on race and income levels.
2. Patients with Medicaid experienced higher out-of-pocket costs compared to those with private insurance.
3. Financial toxicity was most prevalent among patients with lung and colon cancers.


### **Model Performance**

- Best Model: LightGBM achieved the highest efficiency while maintaining competitive accuracy.

- Feature Importance: Family income had the highest predictive power. Insurance type and prescription type were also significant predictors. Generally, the rest of features had very similar importance.

- Feature Correlation Heatmap: Features are less likely to be correlated with each other， which leads to poor model training.

![image5](https://github.com/user-attachments/assets/ff12074d-f6ff-4e6e-a1dd-2cfa5816d981)


### **Predictive Dashboard**
![image6](https://github.com/user-attachments/assets/3528ad21-1fcd-455c-b04f-1b8dafbd15ca)
An interactive dashboard was developed to:

1. Visualize financial toxicity risks based on user input.
2. Allow stakeholders to explore trends across demographics and regions.




**Key Findings**

1. Financial toxicity is highest among uninsured patients and those with Medicaid.

2. Patients from the South and Midwest regions exhibit higher financial toxicity.

3. Individuals with lower educational attainment and household income are at greater risk.

4. Lung cancer patients face the highest financial toxicity compared to other cancer types.




## **Conclusion**

**1. Demographic and Regional Biases:**

- There are clear indications of racial and regional disparities in insurance coverage, with minority groups and residents in the South being more reliant on public insurance types (e.g., Medicaid, Medicare). These patterns align with known socio-economic disparities and healthcare access inequities.


**2. Economic Disparities:**

- Low-income groups face disproportionately higher financial toxicity, as indicated by their higher total out-of-pocket expenses. This suggests a pressing need for policies targeting affordability for economically vulnerable populations.


**3. Employment and Education Effects:**

- Employment status significantly affects insurance type and coverage, highlighting the importance of stable jobs in accessing private insurance.

- Educational attainment correlates with reduced costs, suggesting that higher education indirectly mitigates financial toxicity through better employment opportunities.


**4. Insignificant Factors:**

- Age and family size show limited or no significant influence on treatment costs. This implies that cancer costs are more strongly driven by systemic factors (insurance, income, region) than by personal demographics like age or household composition.

Our project highlights significant disparities in cancer treatment costs and their financial burden on specific demographic groups. By integrating EDA and predictive modeling into an interactive tool, we aim to empower patients and inform policymakers about actionable steps to reduce financial toxicity.




## **How to Build and Run the Code**

### **Prerequisites**

- Python 3.9+

- Required packages: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `plotly, flask,dash, scipy`.


### **Steps**

1. Clone the repository:\
   bash\
   `git clone `[`https://github.com/KluelessKat/CS506-Final-Project.git`](https://github.com/KluelessKat/CS506-Final-Project.git)``

<!---->

    cd KluelessKat/CS506-Final-Project.git

2. Install dependencies:\
   bash\
   `make install`

3) Run the web application:\
   bash\
   `make run`

4. Access the application at [http://localhost:3000].





## **References**

1. MEPS Data Documentation: [https://meps.ahrq.gov]

2. Project GitHub Repository: [https://github.com/KluelessKat/CS506-Final-Project.git]
