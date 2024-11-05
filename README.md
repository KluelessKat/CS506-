# CS 506 Final Project: Predicting Cancer Treatment Costs and Evaluating Cost-Effectiveness of Terminal Stage Care

## Motivation

The rising costs of cancer treatment place an increasing financial burden on healthcare systems. This project aims to predict future cancer treatment costs and assess the financial viability of continuing care in terminal stages across various cancer types. By evaluating if the **Continuing Phase Cost** remains lower than the **Last Year of Life Cost**, this analysis could provide critical insights for policymakers on whether resources are best utilized during late-stage cancer treatment.

## Data Collection

The dataset is sourced from the [National Cancer Institute's estimates](https://data.world/xprizeai-health/expenditures-for-cancer-care) on cancer care expenditures in the United States. It contains annual expenditure estimates for 2010 through 2020, segmented by cancer site, treatment phase, and various assumptions on incidence and survival trends:
  - **Base Case**: Incidence and survival rates are assumed constant.
  - **Trend Incidence**: Incidence follows recent trends, while survival remains constant.
  - **Trend Survival**: Survival follows recent trends, with constant incidence.
  - **Trend Incidence & Survival**: Both incidence and survival are projected based on recent trends.

This data provides a basis for predicting cancer treatment costs under different scenarios, allowing for nuanced insights into how changes in incidence and survival affect financial demands.

## Exploratory Data Analysis (EDA)

### 1. Total Costs Over Time
![Unknown-5](https://github.com/user-attachments/assets/0fdf9a8d-2b5e-4363-a199-9caa9c4340c4)

#### Key Observations:

- **Steady Growth**: The data shows a steady increase in costs, with some years exhibiting sharper growth than others. This could indicate that either treatment costs are rising faster in certain years, or that there may have been external factors such as policy changes or shifts in healthcare utilization affecting costs.
- **Projected Expenditures**: This trend suggests that if growth continues at this rate, future costs could become unsustainable without interventions. This observation stresses the importance of developing cost-efficient treatment strategies, especially as the demand for cancer care increases.
- **Impact of Incidence and Survival Rates**: The cost increases may be partially attributed to rising cancer incidence rates or improved survival rates. Advances in early detection and more effective treatments mean that patients are living longer, requiring ongoing or more frequent treatments, which contribute to the overall rise in costs.
- **Technological and Treatment Advancements**: Medical advancements, including targeted therapies, immunotherapies, and personalized medicine, often come with high price tags. These new treatment options, while beneficial to patient outcomes, add significantly to the overall expenditure, highlighting a trade-off between clinical efficacy and cost.

### 2. Average Total Costs by Incidence and Survival Assumptions
![Unknown-6](https://github.com/user-attachments/assets/9f1132b1-b71d-433a-9353-5f850ccd4efd)

The bar chart comparing **Average Total Costs under Various Incidence and Survival Assumptions** highlights how different trends impact total expenditure:
   - **Incidence follows recent trends, Survival constant**
   - **Incidence constant, Survival follows recent trends**
   - **Both Incidence and Survival follow recent trends**
   - **Survival follows recent trends, Incidence constant**


#### Key Observations
- **Minimal Variation Across Scenarios**: The average total costs do not show substantial differences across the various incidence and survival scenarios, indicating that the overall cost impact is relatively stable regardless of these assumptions.
- **Highest Cost in "Incidence Follows Recent Trend, Survival Constant" Scenario**: The scenario where incidence follows recent trends but survival rates remain constant shows the highest average total costs. This may suggest that increasing cancer incidence is a primary driver of rising expenditures, even without improvements in survival.
- **Lowest Cost in "Survival Follows Recent Trend, Incidence Constant" Scenario**: The scenario with constant incidence but improving survival shows slightly lower average costs. This suggests that advancements in survival may not drastically increase average total costs, possibly due to improved efficiency in treatment over time.
- **Similar Costs in Combined Trends Scenario**: The scenario where both incidence and survival follow recent trends does not exhibit significantly higher costs than scenarios with only one trend. This could imply that the combined effect of increasing incidence and survival trends does not lead to exponential cost growth, possibly due to the balancing effect of treatments becoming more efficient or widely available.
Implications for Cost Management: Since costs appear to increase most significantly with rising incidence rather than with improving survival, preventive measures and early interventions could be more effective in managing total costs over time.

These observations suggest that managing cancer incidence could be a more impactful strategy for controlling overall costs compared to focusing solely on survival improvements.

### 3. Variation in Costs per Cancer Site
![Unknown-7](https://github.com/user-attachments/assets/d8ca74d2-5648-4ac9-9b31-db89267d57ad)

The heatmap of **Costs per Cancer Site** offers a detailed view of expenses associated with different cancer types across treatment phases:
   - **Total Costs**
   - **Initial Year After Diagnosis Cost**
   - **Continuing Phase Cost**
   - **Last Year of Life Cost**

The **Variation in Costs per Cancer Site** heatmap provides several key observations:

   - **High Costs for Colorectal and Lung Cancer**: Colorectal and lung cancer incur some of the highest total costs across all phases (Initial Year After Diagnosis, Continuing Phase, and Last Year of Life). These types of cancer may have higher incidence rates and longer treatment durations, contributing to their significant cost burden.
   
   - **Breast Cancer and Prostate Cancer Have Substantial Initial and Continuing Phase Costs**: While total costs are lower than for some other cancers, breast and prostate cancer show relatively high costs in both the Initial Year After Diagnosis and Continuing Phase. This likely reflects the extensive, long-term treatment and follow-up care required for these cancers.
   
   - **High Last Year of Life Costs for Brain and Esophageal Cancer**: Brain and esophageal cancers exhibit disproportionately high costs in the Last Year of Life phase compared to other phases. These cancers may require more intensive and costly palliative care in their terminal stages.
   
   - **Lower Costs for Melanoma, Uterus, and Stomach Cancer**: These cancer types generally show lower costs across all phases. This may be due to lower incidence rates, shorter treatment durations, or potentially less resource-intensive treatment options.
   
   - **Significant Variation in Cost Distribution by Phase**: Some cancers, like lymphoma and leukemia, have relatively balanced costs across all phases, while others, such as colorectal and lung cancer, show higher costs concentrated in specific phases, particularly the Continuing and Last Year of Life phases.

   - **"Other" Cancer Sites Category Shows High Overall Costs**: The "Other" category, which likely aggregates less common cancers, has a high total cost and Continuing Phase Cost. This may reflect the cumulative impact of multiple, diverse cancer types with varying treatment needs.

These observations suggest that cancer treatment costs are highly variable by cancer type and phase, with specific cancers imposing a heavier financial burden, especially in terminal stages. This highlights the importance of targeted cost-management strategies for high-cost cancer types.

## Decision Tree Analysis
![Unknown-8](https://github.com/user-attachments/assets/a694e844-d753-4eac-8627-2d5af75936d5)

The decision tree model provides insights into the cost-effectiveness of continuing versus stopping treatment based on various cost thresholds. The tree structure reveals several key decision points:

### Primary Decision Node
The root node evaluates the **Continuing Phase Cost** with a threshold of 4853.1, with a relatively balanced sample distribution (562 stop, 692 continue) and a gini impurity of 0.495.

### Left Branch (Continuing Phase Cost ≤ 4853.1)
- Initial split evaluates **Last Year of Life Cost** at 575.05
- For costs below 575.05, treatment is uniformly stopped (61 samples)
- For costs above 575.05, a secondary split at 1879.5 further refines the decision:
  - Moderate costs (575.05-1879.5) show mixed decisions (gini = 0.454)
  - Higher costs (>1879.5) strongly favor continuing treatment (340 continue vs 5 stop)

### Right Branch (Continuing Phase Cost > 4853.1)
- Evaluates **Initial Year After Diagnosis Cost** at 56269.65
- High initial costs (>56269.65) uniformly suggest continuing treatment
- Lower initial costs are further evaluated based on Continuing Phase Cost at 6362.5:
  - Clear decision to stop treatment for costs above 6362.5 (255 samples)
  - Mixed decisions for costs between 4853.1 and 6362.5 (74 samples)

The tree achieves high predictive confidence in several branches, indicated by gini impurity scores of 0.0 in multiple leaf nodes, suggesting strong decision boundaries for certain cost combinations.

## Modeling Approach

### 1. Predicting Cancer Treatment Costs
![Unknown-4](https://github.com/user-attachments/assets/dfe8291a-92d0-46cb-84b5-289d3ff9a33c)

We aim to develop predictive models to estimate future treatment costs based on past trends in incidence, survival, and total expenditures. The models will include:
   - **Linear Regression**: To establish a baseline for cost prediction, using historical data to model linear trends in treatment expenses.
   - **Random Forest or XGBoost**: These models will capture complex, non-linear relationships between costs, incidence, cancer type, and survival trends, potentially providing more accurate predictions than linear regression alone.

### 2. Evaluating Cost-Effectiveness in Terminal Stage Care

To determine the financial feasibility of continuing treatment in terminal stages, we will employ:
   - **Decision Trees**: These models will help visualize and quantify the decision-making process behind continuing or ceasing treatment. By comparing **Continuing Phase Cost** and **Last Year of Life Cost**, the model will provide insights on whether late-stage treatment is financially justified across various cancer types.
   - **Cost-Benefit Analysis**: This analysis will weigh the predicted costs of continued care against projected survival rates, aiming to identify cases where terminal-stage treatment may be cost-effective.

### 3. Trend Analysis for Cancer Sites

The project will also analyze cost patterns across cancer sites, identifying cancer types with rapidly increasing costs and exploring whether these trends are linked to survival improvements or incidence growth. This analysis will help pinpoint specific cancers where targeted interventions could reduce financial strain.

## Future Plan

### Feature Engineering and Selection
We will create the following derived features to enhance our predictive models:
- **Cost Ratios**: Calculate ratios between different treatment phases (Initial/Continuing, Continuing/Last Year) to identify cost-effectiveness patterns
- **Age-Adjusted Costs**: Normalize costs based on age groups to account for demographic variations
- **Annual Growth Rate**: Compute year-over-year growth rates for each cost category
- **Phase Cost Distribution**: Calculate the percentage distribution of costs across treatment phases

### Model Development Strategy

#### 1. Time Series Analysis
- Implement ARIMA and Prophet models to forecast:
  - Total cost trends by cancer site
  - Phase-specific cost projections
  - Annual cost increase patterns

#### 2. Advanced Machine Learning Models
- Develop ensemble models combining:
  - Random Forest for handling non-linear relationships
  - XGBoost for capturing complex patterns in cost variations
  - LightGBM for efficient processing of categorical features
 
### Validation Framework
- Implement temporal validation by:
  - Training on 2010-2018 data
  - Validating on 2019 data
  - Testing on 2020 data
- Use stratified sampling to ensure balanced representation across cancer sites

### Interpretability Analysis
- Deploy [SHAP (SHapley Additive exPlanations)](https://github.com/shap/shap) values to:
  - Identify key cost drivers by cancer site
  - Understand feature importance in treatment phase transitions
  - Analyze the impact of demographic factors on cost patterns

## Project Outcome

Our expected deliverables include:
   1. **Predictive Models**: Models capable of forecasting future cancer treatment costs based on various trends in incidence and survival.
   2. **Cost-Effectiveness Insights**: An evaluation of whether continuing treatment in terminal stages is financially sustainable across different cancer types.
   3. **Healthcare Impact Analysis**: A detailed report with insights that can guide healthcare policymakers in making informed decisions about resource allocation and the cost-benefit of late-stage cancer treatments. 

This analysis is expected to provide actionable insights into cancer treatment costs, potentially informing future policies to make healthcare spending more efficient and impactful.
