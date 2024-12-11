# CS 506 Final Project: Predicting Financial Toxicity for Cancer Patients

## Table of Contents
1. [Project Overview](#project-overview)
2. [Motivation](#motivation)
3. [Data Acquisition, Processing, and Cleaning](#data-acquisition-processing-and-cleaning)
4. [Visualization and Exploratory Data Analysis](#visualization-and-exploratory-data-analysis)
5. [Data Modeling](#data-modeling)
6. [Results](#results)
7. [Conclusion](#conclusion)
8. [How to Build and Run the Code](#how-to-build-and-run-the-code)
9. [References](#references)

---

## Project Overview
This project aims to predict financial toxicity for cancer patients by analyzing the relationship between socio-economic, demographic, and health-related variables. Financial toxicity is measured as the ratio of out-of-pocket expenses to household income. Our goal is to uncover patterns or biases in treatment costs and enable patients, policymakers, and healthcare providers to reduce financial toxicity.

Our tool combines interactive visualizations, EDA, and predictive modeling into a web application, allowing users to explore trends and predict financial toxicity based on input.

---

## Motivation
Cancer treatment costs are a major contributor to financial toxicity, especially for vulnerable populations. Through this project, we:
1. Investigate demographic and regional biases in financial toxicity.
2. Highlight systemic disparities in cancer treatment costs.
3. Provide a predictive tool to inform policymakers and patients.

### Key Insights:
- Rising cancer costs are largely independent of disease progression.
- Financial toxicity disproportionately affects minority groups and economically disadvantaged regions.

---

## Data Acquisition, Processing, and Cleaning
### Data Source
- Data: Medical Expenditure Panel Survey (MEPS) for 2020–2022.
- Key Variables: Demographics, insurance types, cancer diagnoses, and financial metrics.

### Cleaning Steps:
1. **Unifying Columns Across Years**: Standardized variables (e.g., `REGION22` → `region`).
2. **Encoding Categorical Variables**: Race, education, and insurance types converted into meaningful categories.
3. **Filtering for Cancer Patients**: Focused only on individuals diagnosed with cancer (`CANCERDX = 1`).
4. **Handling Financial Data**: Standardized and aggregated total expenses from various sources.

Final processed dataset includes harmonized variables like:
- Demographics (e.g., age, race, region).
- Insurance status (e.g., private, Medicaid, Medicare).
- Out-of-pocket costs and income levels.

---

## Visualization and Exploratory Data Analysis
Interactive visualizations provide insights into key variables:
1. **Amount vs Age**: Treatment costs remain consistent across age groups.
2. **Amount vs Education**: Higher education correlates with lower financial toxicity.
3. **Coverage vs Employment Status**: Private insurance dominates for employed individuals.
4. **Out-of-Pocket vs Income**: Lower-income groups bear the greatest financial burden.
5. **Coverage vs Race**: Minority groups rely more on Medicaid and Medicare.

### Observations:
- Racial and regional disparities in insurance access.
- Economic status and education level significantly affect financial toxicity.
- Age and family size have limited impact on costs.

---

## Data Modeling
### Objective
To predict financial toxicity risk using demographic, insurance, and cancer-specific features.

### Algorithms Explored:
1. **CatBoost Regressor**: RMSE = 1.73, Custom Accuracy = 33.19%.
2. **XGBoost Regressor**: RMSE = 1.84, Custom Accuracy = 34.50%.
3. **LightGBM Regressor**: RMSE = 1.79, Custom Accuracy = 32.53%.

**Final Model**: LightGBM was chosen due to its faster training and comparable accuracy.

### Model Pipeline:
1. Train/Test Split: 70/30.
2. Hyperparameter Tuning: Grid search optimization.
3. Metrics: RMSE, R-squared, Custom Accuracy.

---

## Results
### Data Insights:
1. Private insurance reduces out-of-pocket costs significantly.
2. Financial toxicity is highest among:
   - Patients with Medicaid.
   - Residents in the South and Midwest.
   - Individuals with lower income and education levels.
   - Lung cancer patients.

### Model Performance:
- **Best Model**: LightGBM.
- **Feature Importance**: Income, insurance type, and cancer type were the strongest predictors.

### Interactive Dashboard:
1. Predicts financial toxicity based on user input.
2. Allows exploration of EDA trends.

---

## Conclusion
1. **Demographic Disparities**: Systemic inequities affect minority groups and economically vulnerable regions.
2. **Economic Impact**: Lower-income households face severe financial toxicity.
3. **Actionable Insights**: Policies like Medicaid expansion and subsidies can mitigate disparities.

This project underscores the importance of reducing financial toxicity through targeted interventions and better resource allocation.

---

## How to Build and Run the Code

### Prerequisites:
- Python 3.9+.
- Required libraries: `pandas`, `numpy`, `scikit-learn`, `flask`, `plotly`, `dash`, `scipy`.

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/KluelessKat/CS506-Final-Project.git
   cd CS506-Final-Project
