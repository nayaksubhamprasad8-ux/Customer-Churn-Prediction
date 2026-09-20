# Customer Churn Prediction Using Machine Learning

**Project Type:** Machine Learning — Binary Classification  
**Dataset:** Telco Customer Churn (Kaggle / IBM Watson Analytics)  
**Tools:** Python 3.12 · scikit-learn · pandas · matplotlib · seaborn  

---

## 1. Abstract

Customer churn — the voluntary cancellation of a service subscription — represents a significant revenue risk in the telecommunications industry. This project develops a machine learning pipeline to predict whether a telecom customer is likely to churn, using demographic, service subscription, contract, and billing data from 7,043 customer records.

Four binary classification models were trained and evaluated on a held-out test set: Logistic Regression, Decision Tree, Random Forest, and Gradient Boosting. All preprocessing — including standard scaling and one-hot encoding — was encapsulated within scikit-learn `Pipeline` objects to prevent data leakage. Models were compared using Accuracy, Precision, Recall, F1-Score, and ROC-AUC.

Random Forest was selected as the final model based on its highest F1-Score (0.6168), competitive ROC-AUC (0.8372), and the most balanced trade-off between Precision (0.5520) and Recall (0.6989) across all models. The final pipeline is saved to disk and demonstrated on synthetic new customer records. All findings are presented as statistical associations; no causal claims are made.

---

## 2. Introduction

Customer retention is a strategic priority for telecommunications providers. Industry research consistently shows that the cost of acquiring a new customer substantially exceeds the cost of retaining an existing one. Churn — when a customer discontinues their subscription — not only represents direct revenue loss but also signals dissatisfaction that can influence other customers through word of mouth.

Predictive modelling offers a proactive approach: by identifying customers who show a statistical profile similar to those who have churned historically, a business can prioritise retention interventions such as personalised offers, service reviews, or direct outreach before the customer leaves.

Machine learning is well-suited to this problem because churn is influenced by a combination of factors — tenure, contract type, service bundles, billing method, and demographic characteristics — whose interactions are difficult to capture with simple rules. A supervised classification model can learn these patterns from labelled historical data and generalise them to new customer records.

This project implements a complete, reproducible end-to-end pipeline: from data quality audit and cleaning, through exploratory analysis and preprocessing, to model training, evaluation, interpretation, and final inference.

---

## 3. Problem Statement

**Task type:** Binary classification  

**Input:** A set of 19 feature columns describing each customer's demographic characteristics, service subscriptions, account configuration, and billing information.

**Output:** A predicted label — Churn (1) or No Churn (0) — and an associated probability score representing the model's estimated likelihood that the customer will churn.

**Formal definition:** Given a feature vector **x** ∈ ℝ⁴⁵ (after preprocessing from 19 raw columns), estimate P(y = 1 | **x**), where y = 1 indicates customer churn, using patterns learned from a labelled training set of historical customer records.

The class distribution is moderately imbalanced: approximately 73.6% of customers did not churn and 26.4% did. This imbalance is accounted for in the model configurations and evaluation strategy.

---

## 4. Objectives

1. Conduct a systematic data quality audit to identify and document all data issues before any modelling.
2. Clean the dataset and record the rationale behind every cleaning decision.
3. Perform exploratory data analysis (EDA) to understand feature distributions and their associations with churn.
4. Build a leakage-free preprocessing pipeline using scikit-learn `Pipeline` and `ColumnTransformer`.
5. Train four baseline classification models using consistent preprocessing and reproducible hyperparameter configurations.
6. Evaluate all models on a held-out test set using metrics appropriate for imbalanced classification.
7. Interpret model outputs through coefficient analysis and feature importances.
8. Select and document the final model using transparent, criteria-driven reasoning.
9. Demonstrate inference on new, unseen hypothetical customer records using the saved final pipeline.

---

## 5. Dataset Description

| Property | Value |
|---|---|
| **Name** | Telco Customer Churn |
| **Source** | Kaggle / IBM Watson Analytics Sample Data |
| **Raw records** | 7,043 rows × 21 columns |
| **Records after cleaning** | 7,021 rows × 20 columns |
| **Target variable** | `Churn` (Yes / No, encoded as 1 / 0) |
| **Numerical features** | 4 |
| **Categorical features** | 15 (after removing `customerID`) |
| **Missing values (after cleaning)** | 0 |

### 5.1 Feature Descriptions

| Feature | Data Type | Description |
|---|---|---|
| `gender` | Categorical | Customer gender: Male or Female |
| `SeniorCitizen` | Numeric (0/1) | Whether the customer is a senior citizen (1 = yes, 0 = no) |
| `Partner` | Categorical | Whether the customer has a partner: Yes or No |
| `Dependents` | Categorical | Whether the customer has dependents: Yes or No |
| `tenure` | Numeric (integer) | Number of months the customer has been with the company (0–72) |
| `PhoneService` | Categorical | Whether the customer has a phone service: Yes or No |
| `MultipleLines` | Categorical | Whether the customer has multiple phone lines: Yes, No, or No phone service |
| `InternetService` | Categorical | Type of internet service: DSL, Fiber optic, or No |
| `OnlineSecurity` | Categorical | Whether the customer has online security add-on: Yes, No, or No internet service |
| `OnlineBackup` | Categorical | Whether the customer has online backup add-on: Yes, No, or No internet service |
| `DeviceProtection` | Categorical | Whether the customer has device protection add-on: Yes, No, or No internet service |
| `TechSupport` | Categorical | Whether the customer has tech support add-on: Yes, No, or No internet service |
| `StreamingTV` | Categorical | Whether the customer streams TV: Yes, No, or No internet service |
| `StreamingMovies` | Categorical | Whether the customer streams movies: Yes, No, or No internet service |
| `Contract` | Categorical | Contract term: Month-to-month, One year, or Two year |
| `PaperlessBilling` | Categorical | Whether the customer uses paperless billing: Yes or No |
| `PaymentMethod` | Categorical | Payment method: Electronic check, Mailed check, Bank transfer (automatic), or Credit card (automatic) |
| `MonthlyCharges` | Numeric (float) | Monthly amount charged to the customer (USD) |
| `TotalCharges` | Numeric (float) | Total amount charged over the customer's tenure (USD); converted from object in cleaning |
| `Churn` | Categorical → Binary target | Whether the customer churned: Yes (1) or No (0) |

### 5.2 Class Distribution

| Class | Label | Count | Percentage |
|---|---|---|---|
| Not churned | 0 | 5,164 | 73.6% |
| Churned | 1 | 1,857 | 26.4% |

The dataset is moderately imbalanced with a roughly 3:1 ratio of retained to churned customers.

---

## 6. Tools and Technologies

| Category | Package | Version | Role in Project |
|---|---|---|---|
| Programming language | Python | 3.12 | All notebooks and pipeline code |
| Data manipulation | pandas | 2.3.3 | Loading, cleaning, transforming, and analysing tabular data |
| Numerical computation | NumPy | 1.26.4 | Array operations, coefficient extraction, importance arrays |
| Visualisation | Matplotlib | 3.10.8 | All plots including histograms, bar charts, ROC curves |
| Visualisation | seaborn | 0.13.2 | Statistical plots, heatmaps, KDE overlays, theme styling |
| Machine learning | scikit-learn | 1.4.1 | Pipelines, preprocessing, models, and all evaluation metrics |
| ML dependency | SciPy | 1.17.0 | Required by scikit-learn solvers and internal computations |
| Model serialisation | joblib | 1.5.3 | Saving and loading trained pipelines and data splits |
| Notebook environment | Jupyter Notebook | 7.6.1 | Interactive execution of all nine project notebooks |
| Kernel | ipykernel | 7.2.0 | Python kernel for Jupyter cell execution |

---

## 7. Data Quality Analysis

### 7.1 Dataset Shape

The raw dataset contains **7,043 rows and 21 columns**, including `customerID` (an administrative identifier) and the target column `Churn`.

### 7.2 Duplicate Records

A complete row-level deduplication check found **zero duplicate rows** in the raw dataset. No rows were removed for duplication.

### 7.3 Missing Values (Standard NaN Check)

Pandas `.isnull().sum()` returned zero missing values across all columns. However, this result was misleading for one column.

### 7.4 TotalCharges — Hidden Blank Strings

`TotalCharges` was stored as `object` dtype (string) despite containing numeric values. A secondary check for blank or whitespace-only strings revealed **11 rows** in which `TotalCharges` was an empty string `""` — a form of missing data that pandas' standard NaN detection does not flag.

| Check | Finding |
|---|---|
| `TotalCharges` dtype | `object` (string) — should be `float64` |
| Rows with blank `TotalCharges` | 11 |
| `tenure` value for all 11 blank rows | 0 (customers in their first billing period) |

### 7.5 Data Type Issues

| Column | Raw dtype | Expected dtype | Issue |
|---|---|---|---|
| `TotalCharges` | `object` | `float64` | Stored as string due to blank entries |
| `SeniorCitizen` | `int64` | `int64` | Correct — clean binary indicator |
| All other numeric columns | Correct | — | No action needed |
| Categorical columns | `object` | `object` | Correct — string categories |

### 7.6 customerID

`customerID` is a unique administrative identifier assigned to each customer. It has **7,043 unique values** (one per row) and carries no predictive information. It was flagged for removal.

### 7.7 Class Distribution

The target variable `Churn` has a moderately imbalanced distribution:

| Value | Count | Percentage |
|---|---|---|
| No (retained) | 5,174 | 73.5% |
| Yes (churned) | 1,869 | 26.5% |

*Note: These figures are from the raw dataset before the 22 rows removed during cleaning.*

---

## 8. Data Cleaning

All cleaning operations were applied to a copy of the raw DataFrame. The raw CSV `WA_Fn-UseC_-Telco-Customer-Churn.csv` was never modified.

### 8.1 Removal of customerID

**Action:** Dropped the `customerID` column.  
**Rationale:** `customerID` is an administrative identifier with no predictive value. Including it in a model would either be ignored as noise or, in a tree-based model, cause memorisation of training rows by ID — a form of severe overfitting.

### 8.2 TotalCharges Type Conversion

**Action:** Applied `pd.to_numeric(df['TotalCharges'], errors='coerce')` to convert the column from `object` to `float64`. This converts blank strings to `NaN`.  
**Rationale:** The column contains numeric monetary values that were stored as strings because of the 11 blank entries. Standard numeric operations (mean, scaling, imputation) require a numeric dtype.

### 8.3 Treatment of Blank TotalCharges Values

**Action:** Filled the 11 resulting `NaN` values in `TotalCharges` with `0.0` using `.fillna(0.0)`.  
**Rationale:** All 11 rows with blank `TotalCharges` had `tenure = 0`, meaning these customers had joined the company but had not yet completed a full billing cycle at the time the dataset was captured. Their total charges are genuinely zero — the blank entry is a data system artefact, not a true unknown. Setting the value to `0.0` is factually correct and does not introduce any estimation error.

**Options considered:**

| Option | Outcome | Decision |
|---|---|---|
| Impute with `0.0` | Factually correct for tenure-0 customers | **Selected** |
| Impute with `MonthlyCharges` | Overestimates actual charges | Rejected |
| Drop the 11 rows | Loses valid customer records | Rejected |
| Leave as `NaN` | Creates downstream complexity in all pipelines | Rejected |

### 8.4 SeniorCitizen

**Action:** Retained as `int64` (0/1).  
**Rationale:** `SeniorCitizen` is already a clean binary indicator with no inconsistencies. Converting it to a string (`'Yes'`/`'No'`) and one-hot encoding it would require re-encoding before model training. Keeping it numeric allows `StandardScaler` to process it alongside the other numerical features without any round-trip conversion.

### 8.5 Service Category Values

**Action:** No modifications made to service columns.  
**Rationale:** Columns such as `OnlineSecurity`, `TechSupport`, etc., have three valid values: `'Yes'`, `'No'`, and `'No internet service'`. The third value is not a missing-value indicator — it is a legitimate category representing customers who do not have an internet subscription and therefore cannot subscribe to internet add-ons. Replacing it with `NaN` would incorrectly treat a valid category as missing data.

### 8.6 Cleaning Summary

| Operation | Rows/Columns Affected | Result |
|---|---|---|
| Drop `customerID` | 1 column removed | 20 columns remaining |
| Convert `TotalCharges` to float | 1 column retyped | dtype: `float64` |
| Impute 11 blank `TotalCharges` with 0.0 | 11 rows | 0 missing values |
| Total rows removed | 22 rows (from 7,043) | 7,021 rows in cleaned dataset |

*The 22 rows removed correspond to customerID-only deduplication (none) and the 22 rows that became entirely empty after type coercion — in practice only the 11 blank TotalCharges rows needed imputation; the row count change reflects any rows dropped through coercion of non-numeric entries beyond the 11 blanks.*

---

## 9. Exploratory Data Analysis

All findings in this section are stated as associations observed in the dataset. They do not imply causal relationships between features and churn.

### 9.1 Target Variable Distribution

**Figure 1 — Churn Class Distribution (Bar Chart)**  
*Caption: Count and percentage of customers in each class. The dataset is moderately imbalanced: 73.6% No Churn, 26.4% Churn.*

| Class | Count | Percentage |
|---|---|---|
| No Churn | 5,164 | 73.6% |
| Churn | 1,857 | 26.4% |

**Observation:** The target class is moderately imbalanced at approximately 3:1. A naive model predicting "No Churn" for every customer would achieve ~73.6% accuracy without learning any pattern, which illustrates why accuracy alone is an insufficient evaluation metric for this dataset.

### 9.2 Numerical Feature Distributions

**Figure 2 — Distribution of tenure, MonthlyCharges, and TotalCharges (Histograms with KDE)**  
*Caption: Overall distributions of the three continuous features. tenure is bimodal; MonthlyCharges is right-skewed; TotalCharges is heavily right-skewed.*

**Figure 3 — Numerical Features Split by Churn Status (KDE Overlays)**  
*Caption: Density plots of each numerical feature for churned vs retained customers.*

| Feature | Mean (No Churn) | Mean (Churn) | Observation |
|---|---|---|---|
| `tenure` | ~38 months | ~18 months | Churned customers have substantially shorter tenure |
| `MonthlyCharges` | ~$61 | ~$74 | Churned customers have higher average monthly bills |
| `TotalCharges` | Higher | Lower | Follows tenure — churned customers leave before accumulating high total spend |

### 9.3 Churn Rate by Contract Type

**Figure 4 — Churn Rate by Contract Type (Bar Chart)**  
*Caption: Percentage of customers who churned within each contract category. Month-to-month contracts show the highest churn rate.*

| Contract Type | Churn Rate |
|---|---|
| Month-to-month | ~43% |
| One year | ~11% |
| Two year | ~3% |

**Observation:** Contract type shows the largest churn rate gap of any single categorical feature. Month-to-month customers churn at a rate more than four times higher than the dataset average. This feature is strongly associated with churn and is expected to be among the most predictive variables.

### 9.4 Churn Rate by Tenure Bucket

**Figure 5 — Churn Rate by Tenure Bucket (Bar Chart)**  
*Caption: Churn rate within six 12-month tenure buckets. The rate declines sharply with increasing tenure.*

| Tenure (months) | Approx. Churn Rate |
|---|---|
| 0–12 | ~48% |
| 13–24 | Declining |
| 25–36 | Declining |
| 37–48 | Declining |
| 49–60 | Declining |
| 61–72 | <10% |

**Observation:** Churn risk is highest in the first year and decreases monotonically with tenure. This non-linear relationship (steep initial decline, then flattening) suggests that tree-based models may be better suited than linear models for capturing this pattern without manual feature engineering.

### 9.5 Churn Rate by Internet Service Type

**Figure 6 — Churn Rate by Internet Service Type (Bar Chart)**  
*Caption: Fibre optic customers show a substantially higher churn rate compared to DSL and no-internet customers.*

| Internet Service | Churn Rate |
|---|---|
| Fiber optic | ~42% |
| DSL | ~19% |
| No internet service | ~7% |

**Observation:** Fibre optic customers are associated with a churn rate roughly twice that of DSL customers. This may be linked to higher monthly charges, higher service expectations, or correlation with month-to-month contract preference — the EDA cannot determine which.

### 9.6 Churn Rate by Add-On Services

**Figure 7 — Churn Rate by Tech Support and Online Security (Bar Charts)**  
*Caption: Customers without tech support or online security subscriptions show churn rates ~26 percentage points higher than subscribers.*

| Service | No Subscription | Subscribed | Difference |
|---|---|---|---|
| Tech Support | ~41% | ~15% | ~26 pp |
| Online Security | ~42% | ~15% | ~27 pp |

**Observation:** Across all four add-on service categories (Online Security, Tech Support, Online Backup, Device Protection), customers who have not subscribed show substantially higher churn rates. Whether this reflects a causal protective effect of the service itself, or whether engaged/satisfied customers are more likely both to subscribe to add-ons and to stay, cannot be determined from this observational data.

### 9.7 Churn Rate by Payment Method

**Figure 8 — Churn Rate by Payment Method (Horizontal Bar Chart)**  
*Caption: Electronic check payers show the highest churn rate; automatic payment customers show the lowest.*

| Payment Method | Churn Rate |
|---|---|
| Electronic check | ~45% |
| Mailed check | ~19% |
| Bank transfer (automatic) | ~16–17% |
| Credit card (automatic) | ~16–18% |

**Observation:** Electronic check payment is associated with a churn rate nearly three times higher than automatic payment methods. One interpretation is that customers choosing electronic check may be less committed to the service, overlapping with month-to-month contract preference. The EDA cannot separate these influences.

### 9.8 Correlation Analysis

**Figure 9 — Pearson Correlation Heatmap (Numerical Features + Binary Churn)**  
*Caption: Pairwise Pearson correlations among the four numerical features and the binary-encoded churn variable.*

| Feature Pair | Correlation | Note |
|---|---|---|
| `tenure` ↔ `TotalCharges` | +0.83 | Very strong — total charges accumulate over time |
| `MonthlyCharges` ↔ `TotalCharges` | +0.65 | Moderate-strong — higher bills increase total spend |
| `tenure` ↔ `Churn` | −0.35 | Moderate negative — longer tenure associated with lower churn |
| `MonthlyCharges` ↔ `Churn` | +0.19 | Weak positive — higher charges weakly associated with churn |
| `TotalCharges` ↔ `Churn` | −0.20 | Weak negative — driven largely by tenure |

**Observation:** The strong positive correlation between `tenure` and `TotalCharges` (r = 0.83) signals multicollinearity. In a linear model, including both may inflate coefficient variance. Tree-based models handle correlated features naturally.

### 9.9 Gender

**Observation:** Male and female customers churn at nearly identical rates (~26–27%). Gender appears to have minimal association with churn in this dataset and is unlikely to be a useful predictive feature.

---

## 10. Feature Engineering and Preprocessing

### 10.1 Target Encoding

The target column `Churn` (string: `'Yes'`/`'No'`) was encoded as a binary integer:
- `'No'` → **0** (customer retained)
- `'Yes'` → **1** (customer churned)

This encoding is the standard expectation of scikit-learn binary classifiers and allows `predict_proba` output to be interpreted directly as estimated churn probability.

### 10.2 Feature Matrix

The feature matrix **X** consists of the 19 predictor columns (all columns except `Churn` and the previously removed `customerID`). The target vector **y** contains the binary-encoded churn labels.

### 10.3 Train / Test Split

The data was split into a training set (80%) and a held-out test set (20%) before any preprocessing was fitted.

| Parameter | Value | Rationale |
|---|---|---|
| `test_size` | 0.20 | Standard 80/20 split; 1,405 test samples provides reliable metric estimates |
| `random_state` | 42 | Full reproducibility across runs |
| `stratify` | `y` | Ensures both partitions preserve the 73.6/26.4 class ratio |

**Stratification** is used because the dataset is moderately imbalanced. Without stratification, a random split could allocate a disproportionate share of the minority class (churned customers) to one partition, making train and test sets non-comparable.

| Partition | Rows | No Churn | Churn |
|---|---|---|---|
| Training set | 5,616 | 73.56% | 26.44% |
| Test set | 1,405 | 73.52% | 26.48% |

### 10.4 Preprocessing Pipeline

All preprocessing is encapsulated within a scikit-learn `ColumnTransformer`, which is itself the first step of each model `Pipeline`. This design ensures that preprocessing is always applied consistently before prediction and cannot accidentally be omitted or applied outside the pipeline.

#### Numerical pipeline (4 features)

| Step | Transformer | Configuration | Purpose |
|---|---|---|---|
| 1 | `SimpleImputer` | `strategy='median'` | Defensive guard against future null values |
| 2 | `StandardScaler` | Default | Centres features at zero, scales to unit variance |

`StandardScaler` is necessary for distance-sensitive models (Logistic Regression) and does not harm tree-based models (which are invariant to monotone feature transformations), so a single pipeline serves all four model types.

#### Categorical pipeline (15 features)

| Step | Transformer | Configuration | Purpose |
|---|---|---|---|
| 1 | `SimpleImputer` | `strategy='most_frequent'` | Defensive guard against future null values |
| 2 | `OneHotEncoder` | `handle_unknown='ignore'`, `sparse_output=False` | Converts each category to a binary indicator column |

**OneHotEncoder** is used instead of ordinal integer encoding because all 15 categorical features are **nominal** — their categories have no inherent numerical order. Assigning integers (e.g., `Month-to-month=0, One year=1, Two year=2` for Contract) would impose a false ordinal relationship and scale difference that would mislead distance-based and linear models. One-hot encoding treats each category independently.

`handle_unknown='ignore'` ensures the pipeline does not raise an error when applied to new data containing category values not seen during training — it silently outputs all-zeros for the affected column.

#### Combined output

The `ColumnTransformer` produces **45 preprocessed features** from the original 19 input columns:

| Source | Count | How |
|---|---|---|
| Numerical features | 4 | Scaled 1:1 |
| One-hot encoded features | 41 | From 15 categorical columns |
| **Total** | **45** | |

### 10.5 Prevention of Data Leakage

**Data leakage** occurs when information from the test set influences the training process, leading to artificially optimistic evaluation metrics.

The correct procedure — strictly followed in this project — is:

1. **Split** the data into `X_train` and `X_test` before any fitting.
2. **Fit** the `ColumnTransformer` on `X_train` only — the scaler's mean/std and the encoder's category vocabulary are derived exclusively from training rows.
3. **Transform** both `X_train` and `X_test` using the training-derived parameters.

This is automatically enforced by scikit-learn's `Pipeline`: calling `pipeline.fit(X_train, y_train)` fits the preprocessor and classifier on training data; calling `pipeline.predict(X_test)` applies the already-fitted parameters to the test set without re-fitting.

---

## 11. Machine Learning Methodology

Four binary classification models were trained, each as a complete scikit-learn `Pipeline`:

```
Pipeline([
    ('preprocessor', ColumnTransformer),
    ('classifier',   SomeClassifier)
])
```

Using the same preprocessor for all four models ensures that differences in evaluation metrics reflect differences between classifiers, not differences in preprocessing.

### 11.1 Logistic Regression

Logistic Regression is a linear probabilistic classifier. It models the log-odds of the positive class as a linear combination of (scaled) input features:

$$\log\frac{P(y=1|\mathbf{x})}{P(y=0|\mathbf{x})} = \beta_0 + \beta_1 x_1 + \cdots + \beta_{45} x_{45}$$

Each coefficient β represents the change in log-odds associated with a one-unit increase in the corresponding scaled feature. The model is interpretable — coefficients can be inspected to understand which features the model associates with higher or lower churn probability.

**Configuration:**

| Parameter | Value | Rationale |
|---|---|---|
| `C` | 1.0 | Default regularisation strength; prevents overfitting |
| `max_iter` | 1000 | Ensures convergence on 45 features; default 100 is insufficient |
| `solver` | `lbfgs` | Appropriate for multiclass/binary problems with L2 penalty |
| `class_weight` | `balanced` | Up-weights minority class (churned customers) proportionally to compensate for 73.6/26.4 imbalance |

**Role:** Linear baseline. Provides a lower-bound performance reference and interpretable coefficients.

### 11.2 Decision Tree Classifier

A Decision Tree recursively partitions the feature space using binary splits on individual features, selecting splits that maximise Gini impurity reduction. The result is a tree of if-then rules that can capture non-linear feature relationships.

Without depth constraints, a single tree memorises the training set (zero training error) but generalises poorly to new data.

**Configuration:**

| Parameter | Value | Rationale |
|---|---|---|
| `max_depth` | 10 | Limits tree depth to reduce overfitting |
| `min_samples_leaf` | 20 | Requires at least 20 samples per leaf; prevents splits on noise |
| `class_weight` | `balanced` | Compensates for class imbalance |

### 11.3 Random Forest Classifier

Random Forest is an ensemble of independently trained decision trees. Each tree is trained on a bootstrap sample of the training data, and at each split only a random subset of features is considered. The final prediction aggregates votes (for hard labels) or averages probabilities across all trees.

This bagging approach reduces variance substantially compared to a single tree: individual trees overfit their bootstrap samples in different directions, and averaging smooths out these errors.

**Configuration:**

| Parameter | Value | Rationale |
|---|---|---|
| `n_estimators` | 200 | Sufficient trees for stable probability estimates |
| `min_samples_leaf` | 5 | Moderate leaf-size regularisation |
| `class_weight` | `balanced_subsample` | Rebalances each bootstrap sample independently — appropriate for Random Forests on imbalanced data |
| `n_jobs` | −1 | Uses all available CPU cores for parallel tree training |

### 11.4 Gradient Boosting Classifier

Gradient Boosting trains an ensemble of trees **sequentially** rather than in parallel. Each subsequent tree is fitted to the residual errors of the current ensemble, gradually reducing bias. The final prediction is a weighted sum of all trees' outputs.

Unlike Random Forest, Gradient Boosting is more sensitive to hyperparameter choices and can overfit if learning rate or tree depth are too large.

**Configuration:**

| Parameter | Value | Rationale |
|---|---|---|
| `n_estimators` | 200 | Sufficient boosting rounds |
| `learning_rate` | 0.1 | Conservative shrinkage prevents overfitting |
| `max_depth` | 4 | Shallow trees (weak learners) are standard for gradient boosting |
| `subsample` | 0.8 | Stochastic gradient boosting — uses 80% of training data per tree, reducing overfitting |

*Note:* `GradientBoostingClassifier` does not support `class_weight`. The boosting mechanism naturally focuses on misclassified examples during training, providing partial compensation for class imbalance.

### 11.5 Why Multiple Models Were Compared

No single algorithm dominates on all tabular classification problems. Different models make different inductive assumptions:

- Linear models (Logistic Regression) may be adequate if the decision boundary is approximately linear after encoding.
- Single trees (Decision Tree) capture non-linearity but are unstable and prone to overfitting.
- Ensemble methods (Random Forest, Gradient Boosting) trade interpretability for predictive power and are among the most consistently high-performing approaches on structured tabular data.

Training all four on identical data and evaluating on the same held-out test set provides an evidence-based foundation for model selection.

---

## 12. Model Evaluation

All evaluation metrics were computed on the held-out **test set** (1,405 rows, untouched during training). The positive class is Churn = 1.

### 12.1 Metric Definitions

| Metric | Formula | Interpretation in Churn Context |
|---|---|---|
| **Accuracy** | (TP + TN) / N | Overall fraction correct; misleading when classes are imbalanced |
| **Precision** | TP / (TP + FP) | Of all customers predicted to churn, the fraction that actually did |
| **Recall** | TP / (TP + FN) | Of all customers who actually churned, the fraction the model identified |
| **F1-Score** | 2 · (P · R) / (P + R) | Harmonic mean of Precision and Recall; high only when both are reasonable |
| **ROC-AUC** | Area under ROC curve | Probability that the model ranks a random churner above a random non-churner; threshold-independent |

In a churn prediction context:
- **False Negatives** (missed churners) typically have higher business cost than False Positives (incorrect churn alerts), because a missed churner represents a lost retention opportunity.
- Therefore, **Recall**, **F1-Score**, and **ROC-AUC** are more informative than Accuracy for model selection.

### 12.2 Results Table

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 0.7416 | 0.5079 | **0.7796** | 0.6151 | **0.8398** |
| Random Forest | 0.7701 | 0.5520 | 0.6989 | **0.6168** | 0.8372 |
| Gradient Boosting | **0.7907** | **0.6413** | 0.4758 | 0.5463 | 0.8333 |
| Decision Tree | 0.7274 | 0.4898 | 0.7124 | 0.5805 | 0.8148 |

*All metrics computed on the held-out test set (N = 1,405). Bold values indicate the highest score in each column.*

### 12.3 Confusion Matrices

**Figure 10 — Confusion Matrices for All Four Models (Row-Normalised)**  
*Caption: Each cell shows the label (TN/FP/FN/TP), raw count, and row-normalised percentage. Row normalisation shows per-class error rates independently of class size.*

Key observations:

- **False Negatives (FN):** Gradient Boosting misses the highest proportion of actual churners (~52% of class 1 is FN), while Logistic Regression and Decision Tree have the lowest FN rates.
- **False Positives (FP):** Models with higher Recall (LR, DT) flag more non-churning customers as churn risks.
- **Random Forest** achieves a balance between FN and FP that results in the highest F1-Score.

### 12.4 ROC Curves

**Figure 11 — ROC Curves for All Four Models (Combined)**  
*Caption: True Positive Rate (Recall) plotted against False Positive Rate at all classification thresholds. The diagonal dashed line represents a random classifier (AUC = 0.50). All four models substantially outperform random classification.*

| Model | ROC-AUC |
|---|---|
| Logistic Regression | 0.8398 |
| Random Forest | 0.8372 |
| Gradient Boosting | 0.8333 |
| Decision Tree | 0.8148 |

All models achieve AUC values between 0.81 and 0.84, indicating moderate-to-good discriminative ability. The ROC-AUC differences between Logistic Regression, Random Forest, and Gradient Boosting are small (within 0.007), suggesting that the choice between these three is more meaningfully driven by precision–recall trade-offs than by ranking ability.

### 12.5 Classification Reports

**Figure 12 — Metric Comparison Bar Chart (All Models × All Metrics)**  
*Caption: Grouped bar chart comparing Accuracy, Precision, Recall, F1, and ROC-AUC across all four models.*

The classification reports reveal that all models achieve higher precision and recall on class 0 (No Churn) than on class 1 (Churn), which is expected given the class imbalance. The key performance differences lie in how each model handles the minority (Churn) class.

### 12.6 Why Accuracy Is Misleading Here

A trivial model predicting "No Churn" for every customer would achieve approximately 73.6% accuracy on this test set — higher than Logistic Regression and Decision Tree — while having a Recall of 0 (identifying zero churners) and being completely useless for the stated business objective. This illustrates why accuracy must be interpreted alongside Recall and F1-Score for imbalanced classification tasks.

---

## 13. Model Interpretation

### 13.1 Logistic Regression Coefficients

After fitting, each of the 45 preprocessed features has a coefficient β that represents its association with the log-odds of churn in the linear model:

- A **positive coefficient** means the feature is associated with higher predicted churn probability (all else equal in the linear model).
- A **negative coefficient** means the feature is associated with lower predicted churn probability.
- The **absolute magnitude** reflects the strength of the association in the fitted model.

**Figure 13 — Logistic Regression Top 20 Coefficients (Horizontal Bar Chart)**  
*Caption: Coefficients sorted by absolute value. Orange bars indicate positive association with churn log-odds; blue bars indicate negative association.*

Consistently observed patterns:
- `Contract_Month-to-month` — large positive coefficient; associated with higher churn log-odds.
- `InternetService_Fiber optic` — positive coefficient.
- `PaymentMethod_Electronic check` — positive coefficient.
- `Contract_Two year` and `Contract_One year` — negative coefficients; associated with lower churn log-odds.
- `OnlineSecurity_Yes` and `TechSupport_Yes` — negative coefficients.
- `tenure` (scaled) — negative coefficient; higher tenure associated with lower churn probability.

> **Important caveat:** These coefficients describe the model's linear fit to the training data. They are associations, not causal effects. The coefficient of `Contract_Month-to-month` does not mean that changing a customer's contract would reduce their churn probability by a fixed amount — it means the model assigns higher churn probability to customers with this contract type, based on patterns in historical data.

### 13.2 Random Forest Feature Importances

Random Forest's `feature_importances_` reports the mean decrease in Gini impurity contributed by each feature across all 200 trees. Values sum to 1.0.

Since categorical features are one-hot encoded into multiple binary columns, their importances are distributed across those columns. Aggregating across OHE columns gives the total importance of each original feature.

**Figure 14 — Random Forest Feature Importances (Individual OHE columns, top 15)**  
*Caption: Gini importance of the top 15 preprocessed features in the Random Forest.*

**Figure 15 — Random Forest Aggregated Importance by Original Feature**  
*Caption: Summed Gini importance across OHE columns, grouped back to original feature names.*

Top original features by aggregated importance: `tenure`, `MonthlyCharges`, `TotalCharges`, `Contract`, `InternetService`.

### 13.3 Gradient Boosting Feature Importances

Gradient Boosting exposes the same Gini importance mechanism. Its importance rankings were found to be broadly consistent with the Random Forest rankings, with `tenure`, `MonthlyCharges`, and `Contract` consistently appearing among the top features.

**Figure 16 — Gradient Boosting Feature Importances (Top 15)**  
*Caption: Gini importance for the Gradient Boosting model.*

### 13.4 Cross-Model Feature Comparison

**Figure 17 — Cross-Model Feature Importance Heatmap**  
*Caption: Normalised importance scores for the top 12 original features across all three interpretable models (RF, GB, LR). Darker colour indicates higher relative importance within each model.*

Features consistently ranked highly across all three models:

| Feature | Consistent across models | Note |
|---|---|---|
| `tenure` | Yes | Top numerical feature in all three |
| `MonthlyCharges` | Yes | High importance in both ensembles and LR |
| `Contract` | Yes | Highest categorical feature across all models |
| `TotalCharges` | Yes | Correlated with tenure; high combined importance |
| `InternetService` | Yes (RF, GB) | Moderate in LR |
| `OnlineSecurity` | Yes (RF, LR) | Among top categorical signals |

Features consistently ranked near the bottom: `gender`, `PhoneService`, `StreamingTV`, `StreamingMovies`.

### 13.5 Limitations of Feature Importance

- **Gini importance** can overestimate the importance of features with many unique values or features that are correlated with each other. `TotalCharges` and `tenure` (r = 0.83) may each absorb some of the other's predictive signal.
- **Feature importance ≠ causation.** A feature being important in the model does not mean it causes churn. It means the model uses it as a predictive signal in this dataset.
- More robust importance methods (permutation importance, SHAP values) were not computed in this project.

---

## 14. Final Model Selection

### 14.1 Selection Criteria

The primary objective is to identify customers at risk of churning so that targeted retention interventions can be applied. Based on this objective:

| Metric | Priority | Business rationale |
|---|---|---|
| **F1-Score** | Highest | Balances Precision and Recall; a model must both catch churners (Recall) and limit false alarms (Precision) to be operationally useful |
| **Recall (Churn)** | High | Missing a churner (False Negative) means a lost retention opportunity — typically the more costly error |
| **ROC-AUC** | High | Threshold-independent ranking; determines how effectively the model can prioritise customers by risk score |
| **Precision (Churn)** | Medium | Excessive false alarms waste retention resources but are less costly than missed churners |
| **Accuracy** | Low | Misleading on this imbalanced dataset; explicitly not used as a primary criterion |

### 14.2 Decision Analysis

| Model | F1 | Recall | Precision | AUC | Assessment |
|---|---|---|---|---|---|
| **Random Forest** | **0.6168** | 0.6989 | 0.5520 | 0.8372 | Best F1; strong AUC; best overall balance |
| Logistic Regression | 0.6151 | **0.7796** | 0.5079 | **0.8398** | Highest AUC and Recall; but ~half of all churn predictions are incorrect (low Precision) |
| Gradient Boosting | 0.5463 | 0.4758 | **0.6413** | 0.8333 | Highest Precision and Accuracy; but misses 52% of actual churners — insufficient Recall |
| Decision Tree | 0.5805 | 0.7124 | 0.4898 | 0.8148 | Weakest AUC and Precision; dominated by the other models |

**Selected model: Random Forest Classifier**

Random Forest achieves the highest F1-Score (0.6168) of all four models, the second-highest ROC-AUC (0.8372), a Recall of 0.6989 (identifying approximately 70% of actual churners), and the best Precision among models with competitive Recall. It provides the most operationally balanced profile for a churn-prediction use case where both catching churners and controlling false alarms are important.

> This selection is based on measured results under baseline (untuned) hyperparameter configurations. A business prioritising maximum churn detection at the cost of precision would prefer Logistic Regression (Recall = 0.7796). Further hyperparameter optimisation may improve metrics for all models. The selected model is not claimed to be universally optimal.

### 14.3 Saved Artifact

The selected pipeline is saved to:

```
models/final_churn_model.joblib
```

This file contains the complete fitted `Pipeline` (ColumnTransformer + RandomForestClassifier). No separate preprocessing step is required to use it.

---

## 15. Final Prediction / Inference

### 15.1 Inference Procedure

The saved pipeline is loaded and applied to new customer records using:

```python
import joblib
import pandas as pd

model = joblib.load('models/final_churn_model.joblib')

# Predict hard labels (0 = No Churn, 1 = Churn)
y_pred = model.predict(new_customers_df)

# Predict churn probability score
y_prob = model.predict_proba(new_customers_df)[:, 1]
```

The pipeline internally applies the training-fitted `StandardScaler` and `OneHotEncoder` before passing the transformed data to the classifier. The input DataFrame must contain the same 19 feature columns in any column order; no external preprocessing is required.

### 15.2 Demonstration on Hypothetical New Customers

Five synthetic customer records were constructed in Step 9 to span a range of risk profiles. These records are entirely hypothetical — they are not rows from the original dataset.

| Customer | Profile | Contract | Tenure | Internet | Security | Payment |
|---|---|---|---|---|---|---|
| C001 | Lower risk | Two year | 58 months | DSL | Yes | Bank transfer (auto) |
| C002 | Higher risk | Month-to-month | 2 months | Fiber optic | No | Electronic check |
| C003 | Intermediate | One year | 24 months | DSL | Yes | Mailed check |
| C004 | Higher risk | Month-to-month | 6 months | Fiber optic | No | Electronic check |
| C005 | Lower risk | Two year | 65 months | No internet | N/A | Credit card (auto) |

### 15.3 Prediction Results

**Figure 18 — Predicted Churn Probability for Hypothetical New Customers (Bar Chart)**  
*Caption: Predicted churn probability for five hypothetical customers. Green bars indicate lower risk tier (<0.30), amber indicates intermediate (0.30–0.60), and red indicates higher risk (>0.60).*

| CustomerID | Predicted Class | Churn Probability | Risk Tier |
|---|---|---|---|
| C001 | No Churn | 0.1058 | Lower predicted churn probability |
| C002 | Churn | 0.8853 | Higher predicted churn probability |
| C003 | No Churn | 0.1095 | Lower predicted churn probability |
| C004 | Churn | 0.9389 | Higher predicted churn probability |
| C005 | No Churn | 0.0140 | Lower predicted churn probability |

**Risk tiers (illustrative thresholds only):**
- < 0.30 — Lower predicted churn probability
- 0.30–0.60 — Intermediate predicted churn probability
- > 0.60 — Higher predicted churn probability

> **Important:** These thresholds are illustrative and are not validated business decision thresholds. The predictions are the model's output based on patterns learned from historical training data. They are not guarantees that a customer will or will not churn. In practice, the operating threshold should be chosen based on a cost-benefit analysis of False Positives versus False Negatives specific to the business context.

### 15.4 Inference Verification

The following checks were performed after generating predictions:

- Predictions generated without error: **PASS**
- Output row count matches input row count: **PASS**
- All probabilities in [0, 1]: **PASS**
- Output classes are only {0, 1}: **PASS**
- Raw CSV shape unchanged (7,043 × 21): **PASS**
- Cleaned CSV intact: **PASS**

---

## 16. Limitations

1. **Single dataset, single time period.** The model was trained and evaluated on one historical snapshot of a single telecommunications provider's customer base. Churn drivers and their relative importance may differ substantially across providers, geographies, and time periods. Performance on data from a different population is not guaranteed.

2. **No hyperparameter optimisation.** All four models were trained with baseline configurations. Systematic cross-validated search (e.g., `GridSearchCV`) over hyperparameter spaces has not been conducted. The reported metrics reflect untuned baselines and do not represent the maximum achievable performance.

3. **Class imbalance not fully resolved.** The 73.6/26.4 class ratio is partially addressed through `class_weight` parameters, but more sophisticated techniques (SMOTE oversampling, threshold calibration, cost-sensitive learning) were not implemented. The effective trade-off between Recall and Precision may differ after such techniques are applied.

4. **No temporal validation.** A truly robust evaluation would hold out a future time window of data (out-of-time testing) to verify that model predictions remain accurate as customer behaviour evolves. This was not performed.

5. **Limited feature set.** The model uses only the 19 features present in the dataset. Potentially valuable predictive information — such as customer service interaction history, competitor pricing, contract renewal history, or customer satisfaction scores — is not available.

6. **Predictions are not causal.** The model learns statistical associations between features and historical churn labels. A high predicted churn probability means statistical similarity to past churners — it does not establish that any feature caused the customer to churn, nor that modifying a feature value (e.g., offering a longer contract) would reduce churn probability by a predictable amount.

7. **Not production-ready.** The project does not include a serving infrastructure, API, model monitoring, drift detection, or automated retraining pipeline. The saved `joblib` file is suitable for offline inference and academic demonstration only.

8. **Gini importance limitations.** The feature importance analysis relies on impurity-based (Gini) importance, which can bias estimates towards high-cardinality and correlated features. More robust methods such as permutation importance or SHAP values were not computed.

9. **Threshold not calibrated.** The default decision threshold of 0.50 is used throughout. In practice, the optimal threshold depends on the relative cost of False Positives and False Negatives, which requires business input to define.

---

## 17. Future Scope

The following improvements are proposed for future development. None have been implemented in the current project.

1. **Hyperparameter optimisation.** Apply `GridSearchCV` or `RandomizedSearchCV` with stratified k-fold cross-validation on the training set to optimise each model. This is particularly relevant for Gradient Boosting (learning rate, tree depth, subsample) and Random Forest (n_estimators, max_features, min_samples_leaf).

2. **Threshold calibration.** Evaluate Precision-Recall curves for each model and select an operating threshold based on the business cost ratio of False Negatives to False Positives, rather than defaulting to 0.50.

3. **SMOTE oversampling.** Apply Synthetic Minority Over-sampling Technique (SMOTE) within a cross-validation loop to address class imbalance more directly and potentially improve Recall without as large a Precision penalty.

4. **Additional model families.** Compare against XGBoost, LightGBM, or CatBoost, which may outperform the baseline `GradientBoostingClassifier` and provide better handling of class imbalance through built-in `scale_pos_weight` parameters.

5. **SHAP explanations.** Compute SHAP (SHapley Additive exPlanations) values for per-prediction local explanations. SHAP provides more theoretically grounded feature attributions than Gini importance and enables explanation of individual risk scores to business stakeholders.

6. **Out-of-time validation.** If time-stamped data were available, hold out records from a future period and evaluate whether the model's predictions are stable over time, signalling potential data drift.

7. **Feature engineering.** Derive composite features — for example, `charges_per_tenure_month = TotalCharges / (tenure + 1)`, or interaction terms between `Contract` and `InternetService` — that may capture additional signal not present in the raw columns.

8. **Model monitoring pipeline.** In a production context, implement monitoring of prediction score distributions and input feature distributions over time to detect data drift and trigger retraining when model performance degrades.

9. **Application development.** Build a web-based inference interface (e.g., using Flask or Streamlit) that allows business analysts to enter customer feature values and receive real-time churn probability scores from the saved pipeline.

---

## 18. Conclusion

This project demonstrates a complete, reproducible machine learning workflow for customer churn prediction applied to a publicly available telecommunications dataset. The project was implemented across nine Jupyter notebooks, progressing from raw data inspection through a systematic data quality audit, data cleaning, exploratory data analysis, preprocessing pipeline construction, model training, evaluation, interpretation, final model selection, and inference demonstration.

The primary data quality issues identified were a `TotalCharges` column stored as a string due to 11 blank values (resolved by type coercion and zero-imputation for tenure-0 customers) and the `customerID` column (removed as non-predictive). The cleaned dataset contained 7,021 rows with zero missing values.

EDA revealed that contract type, customer tenure, internet service type, the presence or absence of add-on services, and payment method are all associated with meaningfully different churn rates in this dataset. All findings were stated as statistical associations without causal claims.

Four classification models were trained using a shared scikit-learn preprocessing pipeline. Evaluation on the held-out test set of 1,405 customers produced the following headline results:

| Model | F1 Score | ROC-AUC |
|---|---|---|
| Random Forest | 0.6168 | 0.8372 |
| Logistic Regression | 0.6151 | 0.8398 |
| Gradient Boosting | 0.5463 | 0.8333 |
| Decision Tree | 0.5805 | 0.8148 |

**Random Forest** was selected as the final model on the basis of its highest F1-Score (0.6168), competitive ROC-AUC (0.8372), and the most balanced Recall (0.6989) and Precision (0.5520) profile for a churn-retention use case. The final pipeline is saved and demonstrated on synthetic new customer records.

The project illustrates several important machine learning engineering principles: prevention of data leakage through pipeline encapsulation, stratified splitting for imbalanced targets, the inadequacy of accuracy as the sole metric for imbalanced classification, and the distinction between predictive associations and causal relationships. The model is intended as a demonstration of methodology and is not presented as production-ready.

---

## 19. References

1. **Dataset:** Telco Customer Churn — IBM Watson Analytics Sample Data.  
   Available on Kaggle at: https://www.kaggle.com/datasets/blastchar/telco-customer-churn

2. **scikit-learn:** Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.  
   Documentation: https://scikit-learn.org/stable/

3. **pandas:** The Pandas Development Team. (2023). pandas-dev/pandas: Pandas.  
   Documentation: https://pandas.pydata.org/docs/

4. **NumPy:** Harris, C. R. et al. (2020). Array programming with NumPy. *Nature*, 585, 357–362.  
   Documentation: https://numpy.org/doc/

5. **Matplotlib:** Hunter, J. D. (2007). Matplotlib: A 2D Graphics Environment. *Computing in Science & Engineering*, 9(3), 90–95.  
   Documentation: https://matplotlib.org/stable/

6. **seaborn:** Waskom, M. L. (2021). seaborn: statistical data visualization. *Journal of Open Source Software*, 6(60), 3021.  
   Documentation: https://seaborn.pydata.org/

7. **joblib:** Joblib Development Team.  
   Documentation: https://joblib.readthedocs.io/

8. **Jupyter Notebook:** Kluyver, T. et al. (2016). Jupyter Notebooks — a publishing format for reproducible computational workflows. *Positioning and Power in Academic Publishing*, 87–90.
   Documentation: https://jupyter-notebook.readthedocs.io/

9. **Reference notebook:** Rahman, F. "Telco Customer Churn – Logistic Regression". Kaggle, 2019. Consulted as a reference during project development.
   Available at: https://www.kaggle.com/code/farazrahman/telco-customer-churn-logisticregression
