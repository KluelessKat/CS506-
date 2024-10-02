# CS 506 Final Project: Predicting Cancer Treatment Costs and Evaluating Cost-Effectiveness of Terminal Stage Care

## Motivation
The goal is to predict future cancer treatment costs and evaluate whether continuing treatment during terminal stages across various cancer types is financially justifiable.

## Data Collection
The data will be sourced from the [National Cancer Institute's estimates](https://data.world/xprizeai-health/expenditures-for-cancer-care) on cancer care expenditures in the U.S. The dataset includes expenditure estimates for 2010 and 2020, broken down by cancer site, and considers different assumptions:
  - **Base Case**: Constant incidence and survival rates
  - **Trend Incidence**: Projected incidence trends with constant survival
  - **Trend Survival**: Constant incidence with projected survival trends
  - **Trend Incidence & Survival**: Both incidence and survival trends are projected

This data will provide a foundation for building models that predict cancer treatment costs under varying conditions.

## Modeling Approach
Our primary objective is to predict cancer treatment costs based on the trends in incidence and survival. We will employ the following approaches:
  1. **Linear Regression**: To model treatment costs based on past expenditures and survival rates. It will serve as a baseline model.
  2. **Random Forest or XGBoost**: These more sophisticated regression techniques will allow us to capture complex relationships between cost, incidence, cancer type, and survival trends.
  3. **Cost-Benefit Analysis**: Using decision trees, we will evaluate the financial worth of continuing cancer treatment in the terminal stages of the disease by considering predicted costs against projected survival rates. Potentially, different decision trees could be created encompassing the condition of varied cancer types.
  4. **Trend Analysis for Cancer Sites**: We will investigate patterns in treatment costs across different cancer sites, identifying which cancer types have rapidly increasing costs and whether these are tied to survival rates or incidence trends.

## Visualization
We plan to use the following visualization techniques:
  1. **Bar and Line Charts**: To show trends in cancer treatment costs over time, highlighting differences under various scenarios (e.g., base case vs. projected trends).
  2. **Scatter Plots**: Visualizing relationships between cancer incidence, survival, and costs to illustrate key patterns.
  3. **Decision Trees**: To visually represent the outcomes of continuing vs. stopping treatment in terminal stages, helping to clarify cost-effectiveness.
  4. **Heatmaps**: To display the variation in costs per cancer site, helping to identify which cancers contribute the most to rising healthcare expenditures.

## Test Plan
To validate the model's performance, we will:
  1. **Train-Test Split**: Withhold 20% of the data for testing while training on the remaining 80%.
  2. **Cross-Validation**: Apply k-fold cross-validation (e.g., k=5) to ensure model robustness.
  3. **Performance Metrics**: Use Mean Absolute Error (MAE) and Root Mean Square Error (RMSE) to evaluate prediction accuracy, and feature importance scores to understand key predictors of rising costs.

## Project Outcome
The project aims to deliver:
  1. **Predictive Models**: A model capable of predicting future cancer treatment costs based on various trends in incidence and survival.
  2. **Cost-Effectiveness Insights**: An evaluation of whether continuing treatment in terminal stages is financially justified.
  4. **Impactful Insights for Healthcare**: A detailed analysis that could guide healthcare policymakers to more effectively make decisions regarding the cost and benefit of late-stage cancer treatments across cancer types.
