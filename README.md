# Customer Churn Prediction Using Machine Learning

A complete, end-to-end machine learning project that predicts customer churn for a telecommunications provider. The project covers the full data science workflow — from raw data exploration and cleaning through model training, evaluation, interpretation, and inference — implemented across nine structured Jupyter notebooks.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Objectives](#3-objectives)
4. [Dataset](#4-dataset)
5. [Technologies Used](#5-technologies-used)
6. [Project Workflow](#6-project-workflow)
7. [Data Preprocessing](#7-data-preprocessing)
8. [Exploratory Data Analysis](#8-exploratory-data-analysis)
9. [Machine Learning Models](#9-machine-learning-models)
10. [Model Evaluation](#10-model-evaluation)
11. [Final Model](#11-final-model)
12. [Example Prediction](#12-example-prediction)
13. [Project Structure](#13-project-structure)
14. [Installation](#14-installation)
15. [How to Run](#15-how-to-run)
16. [Limitations](#16-limitations)
17. [Future Improvements](#17-future-improvements)
18. [Conclusion](#18-conclusion)

---

## 1. Project Overview

This project builds a binary classification model to predict whether a telecommunications customer is likely to churn (cancel their service). Starting from a raw CSV dataset, the project progresses through a documented, reproducible workflow: data quality audit, cleaning, exploratory data analysis, feature engineering, model training, evaluation, and final inference.

The output is a trained scikit-learn `Pipeline` that accepts raw customer feature data and returns a predicted churn label (0 = No Churn, 1 = Churn) along with a probability score.

---

## 2. Problem Statement

Customer churn — when a customer stops using a service — is a significant business problem in the telecommunications industry. Acquiring a new customer typically costs more than retaining an existing one. If a model can identify customers who are at risk of churning before they leave, the business can direct targeted retention efforts towards those customers.

This project addresses the following question:

> **Given a set of customer features (contract type, service subscriptions, tenure, billing information, and demographics), can we predict which customers are likely to churn?**

---

## 3. Objectives

- Perform a systematic data quality audit on the raw dataset.
- Clean the dataset and document every decision made.
- Conduct an exploratory data analysis (EDA) to understand the distribution of features and their association with churn.
- Build a reproducible scikit-learn preprocessing pipeline that prevents data leakage.
- Train four baseline classification models and compare their performance on a held-out test set.
- Select a final model based on documented, criteria-driven reasoning.
- Demonstrate inference on new, unseen customer records using the saved final model pipeline.

---

## 4. Dataset

| Property | Value |
|---|---|
| **Name** | Telco Customer Churn |
| **Source** | Kaggle / IBM Watson Analytics Sample Data |
| **Raw records** | 7,043 rows × 21 columns |
| **Records after cleaning** | 7,021 rows × 20 columns |
| **Target variable** | `Churn` (Yes / No → encoded as 1 / 0) |

### Features

The dataset contains information about each customer's:

- **Demographics:** `gender`, `SeniorCitizen`, `Partner`, `Dependents`
- **Account details:** `tenure` (months), `Contract`, `PaperlessBilling`, `PaymentMethod`, `MonthlyCharges`, `TotalCharges`
- **Services subscribed:** `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`

### Class distribution (after cleaning)

| Churn | Count | Percentage |
|---|---|---|
| No (0) | 5,164 | 73.6% |
| Yes (1) | 1,857 | 26.4% |

The dataset is moderately imbalanced with approximately 3:1 ratio of retained to churned customers.

---

## 5. Technologies Used

| Category | Package | Version (used in development) |
|---|---|---|
| Data manipulation | `pandas` | 2.3.3 |
| Numerical computation | `numpy` | 1.26.4 |
| Visualisation | `matplotlib` | 3.10.8 |
| Visualisation | `seaborn` | 0.13.2 |
| Machine learning | `scikit-learn` | 1.4.1 |
| ML dependency | `scipy` | 1.17.0 |
| Model serialisation | `joblib` | 1.5.3 |
| Notebook server | `notebook` | 7.6.1 |
| Notebook kernel | `ipykernel` | 7.2.0 |

**Language:** Python 3.12  
**Environment:** Jupyter Notebook

---

## 6. Project Workflow

```
Raw Dataset  (WA_Fn-UseC_-Telco-Customer-Churn.csv — never modified)
    │
    ▼
Step 1 — Data Understanding
    Loaded and inspected the raw CSV: shape, dtypes, sample rows,
    column descriptions, and initial observations.
    │
    ▼
Step 2 — Data Quality Audit
    Checked for missing values, blank strings, type inconsistencies,
    duplicate rows, and outliers. Identified 11 blank TotalCharges
    entries and the customerID column as non-predictive.
    │
    ▼
Step 3 — Data Cleaning                       → data/telco_churn_cleaned.csv
    Dropped customerID. Coerced TotalCharges to float64 using
    pd.to_numeric(errors='coerce'). Imputed the 11 blank TotalCharges
    values with 0.0 (all had tenure = 0, justified by billing logic).
    Output: 7,021 rows × 20 columns, zero missing values.
    │
    ▼
Step 4 — Exploratory Data Analysis
    Analysed target distribution, numerical feature distributions,
    categorical churn rates, specific feature–churn relationships,
    and a correlation heatmap. Documented 8 key EDA findings.
    │
    ▼
Step 5 — Feature Engineering & Preprocessing    → data/preprocessed_splits.pkl
    Defined X (19 features) and y (binary). Applied a stratified
    80/20 train/test split (random_state=42). Built a ColumnTransformer
    with a numerical pipeline (SimpleImputer → StandardScaler) and a
    categorical pipeline (SimpleImputer → OneHotEncoder). The
    transformer was defined but NOT fitted — fitting happens inside
    each model pipeline to prevent data leakage.
    │
    ▼
Step 6 — Model Training                          → data/trained_models.pkl
    Trained four scikit-learn Pipelines (preprocessor → classifier)
    exclusively on X_train / y_train:
    Logistic Regression, Decision Tree, Random Forest, Gradient Boosting.
    │
    ▼
Step 7 — Model Evaluation
    Evaluated all four models on the untouched X_test / y_test using
    Accuracy, Precision, Recall, F1-Score, and ROC-AUC. Created
    confusion matrices, classification reports, ROC curves, and
    metric comparison charts.
    │
    ▼
Step 8 — Model Interpretation & Final Selection  → models/final_churn_model.joblib
    Analysed Logistic Regression coefficients and Random Forest /
    Gradient Boosting feature importances. Built a cross-model feature
    importance comparison. Selected Random Forest as the final model
    based on documented criteria.
    │
    ▼
Step 9 — Final Inference
    Loaded final_churn_model.joblib. Ran predictions and probability
    scores on 5 hypothetical new customer records. Verified the
    inference pipeline and confirmed the raw CSV was not modified.
```

---

## 7. Data Preprocessing

### Cleaning decisions (Step 3)

| Issue | Decision | Rationale |
|---|---|---|
| `customerID` column | Dropped | Arbitrary identifier with no predictive value |
| `TotalCharges` stored as `object` | Converted to `float64` via `pd.to_numeric(errors='coerce')` | Column contains numeric values but was read as string |
| 11 blank `TotalCharges` entries | Imputed with `0.0` | All 11 rows had `tenure = 0` — customers who had not yet completed a billing cycle; zero is factually correct |
| Duplicate rows | None found | No action required |
| `SeniorCitizen` (0/1 integer) | Kept as numeric | Already clean binary indicator; round-tripping to string and back would be unnecessary |

### Preprocessing pipeline (Step 5)

All preprocessing is encapsulated in a scikit-learn `ColumnTransformer` inside each model `Pipeline`:

**Numerical features** (`SeniorCitizen`, `tenure`, `MonthlyCharges`, `TotalCharges`):
- `SimpleImputer(strategy='median')` — defensive guard against any future null values
- `StandardScaler()` — zero-mean, unit-variance scaling required for distance-sensitive models

**Categorical features** (15 columns):
- `SimpleImputer(strategy='most_frequent')` — defensive guard
- `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` — creates binary indicator columns for each category; `handle_unknown='ignore'` gracefully handles unseen categories at inference time

The `ColumnTransformer` produces **45 output features** (4 scaled numerical + 41 one-hot encoded) from the original 19 input columns.

### Data leakage prevention

The train/test split is performed **before** the `ColumnTransformer` is fitted. Each model `Pipeline` calls `.fit(X_train, y_train)`, which fits the scaler and encoder exclusively on training data. When `.predict(X_test)` is called, the already-fitted training parameters are applied to the test set — the test set never influences the transformation parameters.

### Train/test split

| Parameter | Value |
|---|---|
| Test fraction | 20% |
| Train fraction | 80% |
| `random_state` | 42 |
| `stratify` | `y` (preserves 73.6/26.4 class ratio in both partitions) |
| Training rows | 5,616 |
| Test rows | 1,405 |

---

## 8. Exploratory Data Analysis

Key findings from Step 4 (stated as associations, not causal claims):

1. **Class imbalance:** ~73.6% of customers did not churn; ~26.4% did. Accuracy alone is a poor evaluation metric for this dataset.

2. **Contract type is strongly associated with churn:** Month-to-month customers show a ~43% churn rate, versus ~11% for one-year and ~3% for two-year contracts.

3. **Shorter tenure is associated with higher churn:** Customers in their first 12 months show a ~48% churn rate; those with 61–72 months show under 10%.

4. **Fibre optic internet is associated with higher churn:** Fibre optic customers churn at ~42% versus ~19% for DSL and ~7% for customers with no internet service.

5. **Customers without add-on services show higher churn rates:** Across Online Security, Tech Support, Online Backup, and Device Protection, customers who have not subscribed show churn rates of 40–42%, compared to 14–16% for subscribers.

6. **Electronic check payment is associated with elevated churn:** ~45% churn rate versus ~16–18% for automatic payment methods.

7. **Higher monthly charges are associated with higher churn:** Customers paying over $90/month churn at ~40%, compared to ~10% for customers paying $30 or less.

8. **Gender shows no meaningful association with churn:** Male and female customers churn at nearly identical rates (~26–27%).

> These findings reflect statistical associations in this dataset and should not be interpreted as causal relationships.

---

## 9. Machine Learning Models

Four baseline models were trained in Step 6, each wrapped in a `Pipeline(preprocessor → classifier)`:

### Logistic Regression
A linear model that estimates the log-odds of churn as a weighted sum of input features. Provides interpretable coefficients and serves as a linear baseline. Configured with `C=1.0`, `max_iter=1000`, `class_weight='balanced'`, and the L-BFGS solver.

### Decision Tree Classifier
A non-linear model that learns axis-aligned decision rules. Prone to overfitting without regularisation; constrained here with `max_depth=10` and `min_samples_leaf=20`. Configured with `class_weight='balanced'`.

### Random Forest Classifier
An ensemble of 200 decision trees trained on bootstrap samples with random feature subsets. Reduces variance compared to a single tree and handles non-linear feature interactions. Configured with `n_estimators=200`, `min_samples_leaf=5`, and `class_weight='balanced_subsample'`.

### Gradient Boosting Classifier
An ensemble that trains trees sequentially, each correcting the errors of the previous. Typically achieves strong precision. Configured with `n_estimators=200`, `learning_rate=0.1`, `max_depth=4`, and `subsample=0.8`.

All models used `random_state=42` for reproducibility.

---

## 10. Model Evaluation

All metrics are computed on the held-out test set (1,405 rows) using scikit-learn. The test set was used **only** for evaluation — it was not involved in training or model selection decisions.

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 0.7416 | 0.5079 | **0.7796** | 0.6151 | **0.8398** |
| Random Forest | 0.7701 | 0.5520 | 0.6989 | **0.6168** | 0.8372 |
| Gradient Boosting | **0.7907** | **0.6413** | 0.4758 | 0.5463 | 0.8333 |
| Decision Tree | 0.7274 | 0.4898 | 0.7124 | 0.5805 | 0.8148 |

*All metrics computed on the positive class (Churn = 1). Results reflect baseline hyperparameter configurations without tuning.*

### Why accuracy alone is misleading here

A naive model that always predicts "No Churn" would achieve ~73.6% accuracy while identifying zero churners (Recall = 0). For this reason, **Recall**, **F1-Score**, and **ROC-AUC** are more informative than accuracy for this imbalanced churn dataset.

---

## 11. Final Model

**Selected model: Random Forest Classifier**

### Selection criteria

The project objective is to identify customers who are likely to churn so that targeted retention interventions can be applied. Based on this objective, metrics were prioritised as follows:

| Metric | Priority |
|---|---|
| **F1-Score** | Highest — balances Precision and Recall; avoids both missing churners and excessive false alarms |
| **Recall** | High — missing a churner (False Negative) typically costs more than a false alarm |
| **ROC-AUC** | High — threshold-independent ranking ability; useful for prioritising customers by risk |
| **Precision** | Medium — too many false alarms waste retention resources |
| **Accuracy** | Low — misleading on this imbalanced dataset |

### Why Random Forest was selected

| Consideration | Detail |
|---|---|
| F1-Score | **0.6168** — highest of all four models |
| Recall | **0.6989** — identifies approximately 70% of actual churners |
| ROC-AUC | **0.8372** — second highest; ranks churners above non-churners ~84% of the time |
| Precision | **0.5520** — meaningfully higher than Logistic Regression (0.5079) |
| Balance | Best overall profile across the four prioritised metrics |

Logistic Regression achieved a slightly higher ROC-AUC (0.8398) and higher Recall (0.7796) but at the cost of substantially lower Precision (0.5079), resulting in roughly half of all churn predictions being incorrect. Gradient Boosting showed the highest Precision (0.6413) but missed 52% of actual churners (Recall = 0.4758), making it unsuitable as the primary model for a retention use case.

> This selection is based on measured results under baseline hyperparameters. A different business prioritisation (e.g., maximising Recall at all costs) would favour Logistic Regression. Further improvement through hyperparameter tuning has not been implemented in this project.

### Saved model

The final pipeline is saved to:

```
models/final_churn_model.joblib
```

It contains the complete fitted `Pipeline` (preprocessor + classifier) and requires no separate preprocessing step to use.

---

## 12. Example Prediction

Step 9 demonstrates loading the saved model and running inference on new customer records. The prediction workflow is:

```python
import joblib
import pandas as pd

# Load the complete pipeline
model = joblib.load('models/final_churn_model.joblib')

# Construct a DataFrame with the 19 expected feature columns
new_customer = pd.DataFrame([{
    'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No',
    'Dependents': 'No', 'tenure': 2, 'PhoneService': 'Yes',
    'MultipleLines': 'No', 'InternetService': 'Fiber optic',
    'OnlineSecurity': 'No', 'OnlineBackup': 'No',
    'DeviceProtection': 'No', 'TechSupport': 'No',
    'StreamingTV': 'Yes', 'StreamingMovies': 'Yes',
    'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
    'PaymentMethod': 'Electronic check',
    'MonthlyCharges': 89.10, 'TotalCharges': 178.20
}])

# Hard label: 0 = No Churn, 1 = Churn
prediction = model.predict(new_customer)

# Probability of churn
churn_probability = model.predict_proba(new_customer)[:, 1]
```

The pipeline internally applies all scaling and encoding before passing the data to the classifier. No manual preprocessing is required.

> Predictions reflect patterns learned from historical training data. A high churn probability indicates statistical similarity to customers who churned in the training set — it is not a guarantee that the customer will churn, and it should not be interpreted as a causal statement.

---

## 13. Project Structure

```
Customer_Churn_Project/
│
├── data/
│   ├── WA_Fn-UseC_-Telco-Customer-Churn.csv   # Raw dataset (never modified)
│   ├── telco_churn_cleaned.csv                  # Cleaned dataset (Step 3 output)
│   ├── preprocessed_splits.pkl                  # Train/test splits + preprocessor (Step 5)
│   └── trained_models.pkl                       # Four fitted pipelines (Step 6)
│
├── models/
│   └── final_churn_model.joblib                 # Selected final pipeline (Step 8)
│
├── notebook/
│   ├── step_01_data_understanding.ipynb
│   ├── step_02_data_quality_audit.ipynb
│   ├── step_03_data_cleaning.ipynb
│   ├── step_04_eda.ipynb
│   ├── step_05_feature_engineering.ipynb
│   ├── step_06_model_training.ipynb
│   ├── step_07_model_evaluation.ipynb
│   ├── step_08_model_interpretation.ipynb
│   └── step_09_final_prediction.ipynb
├── report/
│   ├── Project_Report.md                        # Full technical report (Markdown)
│   ├── Subham_Customer_Churn_Project_Report.docx # Formatted Word document report
│   ├── build_docx.py                            # Script to generate the DOCX report
│   ├── render_figures.py                        # Script to generate report figures
│   └── figures/                                 # Visualisation figures embedded in report
│       ├── fig01_churn_distribution.png
│       ├── ... (15 figures)
│       └── fig15_gb_feature_importance.png
│
├── requirements.txt
└── README.md
```

> **Artifact notes:**
> - `data/preprocessed_splits.pkl`, `data/trained_models.pkl`, and `models/final_churn_model.joblib` are generated project artifacts produced by running the notebooks in sequence (Steps 5, 6, and 8).
> - `report/build_docx.py` generates the DOCX report (`Subham_Customer_Churn_Project_Report.docx`).
> - `report/render_figures.py` generates the standalone report figures in `report/figures/`.

---

## 14. Installation

### Prerequisites

- Python 3.10 or higher
- `pip`

### Setup

1. Clone or download the project directory.

2. (Recommended) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   **Activate on Windows:**
   ```bash
   venv\Scripts\activate
   ```

   **Activate on macOS / Linux:**
   ```bash
   source venv/bin/activate
   ```

3. Install all dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Dependencies installed

| Package | Purpose |
|---|---|
| `pandas` | Data loading and manipulation |
| `numpy` | Numerical operations |
| `matplotlib` | Plotting |
| `seaborn` | Statistical visualisation |
| `scikit-learn` | ML models, pipelines, metrics |
| `scipy` | Required by scikit-learn |
| `joblib` | Model serialisation |
| `notebook` | Jupyter Notebook server |
| `ipykernel` | Python kernel for notebooks |
| `python-docx` | Word (.docx) report generation |

---

## 15. How to Run

The notebooks are designed to be run **in order**. Each notebook produces outputs (cleaned CSVs, pkl files, or saved models) that subsequent notebooks depend on.

1. Start the Jupyter Notebook server from the project root:

   ```bash
   jupyter notebook
   ```

2. Open and run each notebook in sequence:

   | Step | Notebook | Depends on |
   |---|---|---|
   | 1 | `step_01_data_understanding.ipynb` | Raw CSV |
   | 2 | `step_02_data_quality_audit.ipynb` | Raw CSV |
   | 3 | `step_03_data_cleaning.ipynb` | Raw CSV → produces `telco_churn_cleaned.csv` |
   | 4 | `step_04_eda.ipynb` | `telco_churn_cleaned.csv` |
   | 5 | `step_05_feature_engineering.ipynb` | `telco_churn_cleaned.csv` → produces `preprocessed_splits.pkl` |
   | 6 | `step_06_model_training.ipynb` | `preprocessed_splits.pkl` → produces `trained_models.pkl` |
   | 7 | `step_07_model_evaluation.ipynb` | `trained_models.pkl` + `preprocessed_splits.pkl` |
   | 8 | `step_08_model_interpretation.ipynb` | `trained_models.pkl` + `preprocessed_splits.pkl` → produces `final_churn_model.joblib` |
   | 9 | `step_09_final_prediction.ipynb` | `final_churn_model.joblib` |

3. In each notebook, select **Kernel → Restart & Run All** to execute all cells from top to bottom.

> Each notebook from Step 5 onwards includes a fallback that rebuilds its dependencies from earlier outputs if a pkl file is not found. This means individual notebooks can also be run in isolation, though running them in order is recommended for reproducibility.

---

## 16. Limitations

1. **Single dataset, single time period.** The model was trained and evaluated on one historical snapshot of a single telecom provider's customer base. Performance may differ on data from a different provider, market, or time period.

2. **No hyperparameter optimisation.** The models use baseline configurations. Systematic cross-validated tuning (e.g., `GridSearchCV`) has not been applied and could improve all metrics.

3. **Class imbalance not fully resolved.** The 73.6/26.4 class ratio is partially addressed through `class_weight='balanced'` / `'balanced_subsample'`, but techniques such as SMOTE oversampling or threshold calibration have not been implemented.

4. **No temporal validation.** The model has not been validated on a future time window (out-of-time test), which is the standard for real-world deployment readiness.

5. **Limited feature set.** The model is constrained to the 19 features in the dataset. Customer lifetime value, support interaction history, or competitor pricing data — if available — could meaningfully improve predictive power.

6. **Predictions are not causal.** A high churn probability score does not mean the associated feature values caused the customer to churn. The model learns statistical associations, not mechanisms. Interpreting the model as causal is not valid.

7. **The model is not production-ready.** There is no API, monitoring, drift detection, or retraining pipeline. The saved `joblib` file is suitable for offline inference and demonstration only.

8. **Feature importance interpretability.** Gini-based importance (used for Random Forest and Gradient Boosting) can overestimate the importance of high-cardinality and correlated features. More robust methods such as SHAP values have not been computed.

---

## 17. Future Improvements

- **Hyperparameter tuning** using `GridSearchCV` or `RandomizedSearchCV` with cross-validation on the training set to optimise each model.
- **Threshold calibration** — select an operating probability threshold based on the relative business cost of False Negatives vs False Positives, rather than using the default 0.5.
- **SMOTE oversampling** applied within a cross-validation loop to address the class imbalance more directly.
- **Out-of-time validation** — hold out a future time period's data to test whether predictive patterns are temporally stable.
- **SHAP values** for per-prediction local explanations, enabling account managers to understand why a specific customer was flagged as high-risk.
- **Model monitoring pipeline** — track prediction score distributions and feature statistics over time to detect data drift in production.
- **Comparison with additional model families** — XGBoost, LightGBM, or a calibrated stacking ensemble.
- **Feature engineering** — create derived features (e.g., `charges_per_month_of_tenure`, interaction terms between contract type and internet service) that may capture additional signal.

---

## 18. Conclusion

This project demonstrates a complete, reproducible machine learning workflow for customer churn prediction using the Telco Customer Churn dataset. The project follows data science best practices throughout: the raw dataset is never modified, all preprocessing is encapsulated inside scikit-learn `Pipeline` objects to prevent data leakage, the test set is used only for final evaluation, and every modelling decision is documented with explicit reasoning.

Four classification models were trained and evaluated on a held-out test set of 1,405 customers. **Random Forest** was selected as the final model based on its best F1-Score (0.6168), strong ROC-AUC (0.8372), and the most balanced trade-off between Recall (0.6989) and Precision (0.5520) across all four models. The final model correctly identifies approximately 70% of customers who actually churned.

The saved pipeline (`models/final_churn_model.joblib`) can be loaded with a single `joblib.load()` call and applied directly to new customer data in the same 19-column format, with no additional preprocessing required.

The results and findings in this project are presented as statistical associations observed in the training data. They should not be interpreted as causal conclusions about customer behaviour. The model is intended as a demonstration of the end-to-end machine learning workflow and is not presented as production-ready.
