"""
Render all key project figures to report/figures/ for inclusion in the Word report.
Uses exact same data and code logic as the project notebooks.
"""
import os, warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

warnings.filterwarnings('ignore')
sns.set_theme(style='whitegrid', palette='muted', font_scale=1.1)
plt.rcParams.update({
    'figure.dpi': 150, 'axes.titlesize': 13, 'axes.labelsize': 11,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 10,
})

OUT = os.path.join(os.path.dirname(__file__), 'figures')
os.makedirs(OUT, exist_ok=True)

CLEAN = os.path.join(os.path.dirname(__file__), '..', 'data', 'telco_churn_cleaned.csv')
df = pd.read_csv(CLEAN)
df['Churned'] = (df['Churn'] == 'Yes').astype(int)
palette = {'Yes': '#dd8452', 'No': '#4c72b0'}

def save(name):
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, name), bbox_inches='tight', dpi=150)
    plt.close()
    print(f'  saved: {name}')

# ── Figure 1: Churn class distribution ───────────────────────────────────────
churn_counts = df['Churn'].value_counts()
churn_pct    = df['Churn'].value_counts(normalize=True) * 100
fig, ax = plt.subplots(figsize=(6, 4))
colors = ['#4c72b0', '#dd8452']
bars = ax.bar(churn_counts.index, churn_counts.values, color=colors, width=0.5, edgecolor='white')
for bar, (label, pct) in zip(bars, churn_pct.items()):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+40,
            f'{int(bar.get_height()):,}\n({pct:.1f}%)', ha='center', fontsize=11, fontweight='bold')
ax.set_title('Figure 1 — Churn Class Distribution', fontweight='bold')
ax.set_xlabel('Churn'); ax.set_ylabel('Number of Customers')
ax.set_ylim(0, churn_counts.max()*1.22)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{int(x):,}'))
sns.despine(); save('fig01_churn_distribution.png')

# ── Figure 2: Numerical distributions ────────────────────────────────────────
num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, col in zip(axes, num_cols):
    sns.histplot(df[col], bins=40, kde=True, ax=ax, color='#4c72b0')
    ax.set_title(col, fontweight='bold'); ax.set_xlabel(col); ax.set_ylabel('Count')
plt.suptitle('Figure 2 — Distributions of Numerical Features', y=1.02, fontsize=13, fontweight='bold')
save('fig02_numerical_distributions.png')

# ── Figure 3: Numerical features split by Churn ──────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, col in zip(axes, num_cols):
    for churn_val, grp in df.groupby('Churn'):
        sns.kdeplot(grp[col], ax=ax, label=f'Churn={churn_val}',
                    color=palette[churn_val], fill=True, alpha=0.25, linewidth=1.8)
    ax.set_title(col, fontweight='bold'); ax.set_xlabel(col); ax.set_ylabel('Density')
    ax.legend(title='Churn')
plt.suptitle('Figure 3 — Numerical Features by Churn Status (KDE)', y=1.02, fontsize=13, fontweight='bold')
save('fig03_numerical_by_churn.png')

# ── Figure 4: Contract type churn rate ───────────────────────────────────────
contract_rate = (df.groupby('Contract')['Churned'].mean().mul(100)
                   .sort_values(ascending=False))
fig, ax = plt.subplots(figsize=(7, 4))
bar_colors = ['#dd8452', '#55a868', '#4c72b0']
ax.bar(contract_rate.index, contract_rate.values, color=bar_colors, edgecolor='white', width=0.5)
for i, (label, val) in enumerate(contract_rate.items()):
    ax.text(i, val+0.8, f'{val:.1f}%', ha='center', fontsize=12, fontweight='bold')
ax.axhline(y=df['Churned'].mean()*100, color='grey', linestyle='--', linewidth=1.2, label='Overall avg')
ax.set_title('Figure 4 — Churn Rate by Contract Type', fontweight='bold')
ax.set_xlabel('Contract Type'); ax.set_ylabel('Churn Rate (%)')
ax.set_ylim(0, 55); ax.legend(); sns.despine(); save('fig04_churn_by_contract.png')

# ── Figure 5: Churn rate by tenure bucket ────────────────────────────────────
df_t = df.copy()
df_t['tenure_bin'] = pd.cut(df_t['tenure'], bins=[0,12,24,36,48,60,72],
    labels=['0–12','13–24','25–36','37–48','49–60','61–72'], include_lowest=True)
tenure_rate = (df_t.groupby('tenure_bin', observed=True)['Churned'].mean().mul(100))
fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(tenure_rate.index, tenure_rate.values, color='#4c72b0', edgecolor='white', width=0.6)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.6,
            f'{bar.get_height():.1f}%', ha='center', fontsize=10)
ax.axhline(y=df['Churned'].mean()*100, color='grey', linestyle='--', linewidth=1.2, label='Overall avg')
ax.set_title('Figure 5 — Churn Rate by Tenure Bucket', fontweight='bold')
ax.set_xlabel('Tenure (months)'); ax.set_ylabel('Churn Rate (%)')
ax.set_ylim(0, 60); ax.legend(); sns.despine(); save('fig05_churn_by_tenure.png')

# ── Figure 6: Internet service churn rate ────────────────────────────────────
internet_rate = (df.groupby('InternetService')['Churned'].mean().mul(100)
                   .sort_values(ascending=False))
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(internet_rate.index, internet_rate.values,
       color=['#dd8452','#55a868','#4c72b0'], edgecolor='white', width=0.5)
for i, (label, val) in enumerate(internet_rate.items()):
    ax.text(i, val+0.6, f'{val:.1f}%', ha='center', fontsize=12, fontweight='bold')
ax.axhline(y=df['Churned'].mean()*100, color='grey', linestyle='--', linewidth=1.2, label='Overall avg')
ax.set_title('Figure 6 — Churn Rate by Internet Service Type', fontweight='bold')
ax.set_xlabel('Internet Service'); ax.set_ylabel('Churn Rate (%)')
ax.set_ylim(0, 55); ax.legend(); sns.despine(); save('fig06_churn_by_internet.png')

# ── Figure 7: Add-on services (TechSupport + OnlineSecurity) ─────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
color_map = {'Yes':'#4c72b0','No':'#dd8452','No internet service':'#55a868'}
for ax, col, title in zip(axes,
        ['TechSupport','OnlineSecurity'],
        ['Tech Support','Online Security']):
    rate = df.groupby(col)['Churned'].mean().mul(100).sort_values(ascending=False)
    bc = [color_map.get(idx,'#999') for idx in rate.index]
    ax.bar(rate.index, rate.values, color=bc, edgecolor='white', width=0.5)
    for i,(label,val) in enumerate(rate.items()):
        ax.text(i, val+0.6, f'{val:.1f}%', ha='center', fontsize=11, fontweight='bold')
    ax.axhline(y=df['Churned'].mean()*100, color='grey', linestyle='--', linewidth=1.2, label='Overall avg')
    ax.set_title(f'Churn Rate by {title}', fontweight='bold')
    ax.set_xlabel(title); ax.set_ylabel('Churn Rate (%)'); ax.set_ylim(0,55); ax.legend()
plt.suptitle('Figure 7 — Churn Rate by Add-On Services', y=1.02, fontsize=13, fontweight='bold')
sns.despine(); save('fig07_churn_by_addons.png')

# ── Figure 8: Payment method churn rate ──────────────────────────────────────
pay_rate = (df.groupby('PaymentMethod')['Churned'].mean().mul(100).sort_values())
fig, ax = plt.subplots(figsize=(8, 4))
bc = ['#4c72b0' if v < 26 else '#dd8452' for v in pay_rate.values]
pay_rate.plot(kind='barh', ax=ax, color=bc, edgecolor='white')
for bar in ax.patches:
    ax.text(bar.get_width()+0.4, bar.get_y()+bar.get_height()/2,
            f'{bar.get_width():.1f}%', va='center', fontsize=10, fontweight='bold')
ax.axvline(x=df['Churned'].mean()*100, color='grey', linestyle='--', linewidth=1.2, label='Overall avg')
ax.set_title('Figure 8 — Churn Rate by Payment Method', fontweight='bold')
ax.set_xlabel('Churn Rate (%)'); ax.set_ylabel(''); ax.set_xlim(0, 55); ax.legend()
sns.despine(); save('fig08_churn_by_payment.png')

# ── Figure 9: Correlation heatmap ────────────────────────────────────────────
df_corr = df[['SeniorCitizen','tenure','MonthlyCharges','TotalCharges','Churned']].copy()
df_corr.rename(columns={'Churned':'Churn (0/1)'}, inplace=True)
corr = df_corr.corr()
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            vmin=-1, vmax=1, linewidths=0.5, ax=ax, annot_kws={'size':11})
ax.set_title('Figure 9 — Pearson Correlation Heatmap\n(Numerical Features + Churn)', fontweight='bold', pad=10)
save('fig09_correlation_heatmap.png')

# ── Figure 10: Confusion matrices ────────────────────────────────────────────
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score
import joblib, copy

MODELS_PKL  = os.path.join(os.path.dirname(__file__), '..', 'data', 'trained_models.pkl')
SPLITS_PKL  = os.path.join(os.path.dirname(__file__), '..', 'data', 'preprocessed_splits.pkl')

num_feats = ['SeniorCitizen','tenure','MonthlyCharges','TotalCharges']
cat_feats = [c for c in df.drop(columns=['Churn','Churned']).columns if c not in num_feats]

splits = joblib.load(SPLITS_PKL)
X_test, y_test = splits['X_test'], splits['y_test']

model_arts = joblib.load(MODELS_PKL)
trained = model_arts['trained_models']
model_names = ['Logistic Regression','Decision Tree','Random Forest','Gradient Boosting']
class_labels = ['No Churn (0)','Churn (1)']

fig, axes = plt.subplots(1, 4, figsize=(20, 4.5))
for ax, name in zip(axes, model_names):
    cm = confusion_matrix(y_test, trained[name].predict(X_test))
    cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)
    annot = np.empty_like(cm, dtype=object)
    cell_labels = [['TN','FP'],['FN','TP']]
    for r in range(2):
        for c in range(2):
            annot[r,c] = f'{cell_labels[r][c]}\n{cm[r,c]:,}\n({cm_norm[r,c]:.1%})'
    sns.heatmap(cm_norm, ax=ax, annot=annot, fmt='', cmap='Blues', vmin=0, vmax=1,
                linewidths=0.8, linecolor='white', cbar=False,
                xticklabels=class_labels, yticklabels=class_labels, annot_kws={'size':9})
    ax.set_title(name, fontweight='bold', fontsize=11)
    ax.set_xlabel('Predicted Label', fontsize=9); ax.set_ylabel('True Label', fontsize=9)
    ax.tick_params(axis='x', rotation=30)
plt.suptitle('Figure 10 — Confusion Matrices (Row-Normalised, Test Set)',
             y=1.03, fontsize=13, fontweight='bold')
save('fig10_confusion_matrices.png')

# ── Figure 11: ROC curves ─────────────────────────────────────────────────────
pal = {'Logistic Regression':'#4c72b0','Decision Tree':'#dd8452',
       'Random Forest':'#55a868','Gradient Boosting':'#c44e52'}
fig, ax = plt.subplots(figsize=(7, 6))
for name in model_names:
    prob = trained[name].predict_proba(X_test)[:,1]
    fpr, tpr, _ = roc_curve(y_test, prob)
    auc = roc_auc_score(y_test, prob)
    ax.plot(fpr, tpr, lw=2, color=pal[name], label=f'{name}  (AUC = {auc:.4f})')
ax.plot([0,1],[0,1],'k--',lw=1.2,label='Random classifier (AUC = 0.50)')
ax.set_xlim([-0.01,1.01]); ax.set_ylim([-0.01,1.05])
ax.set_xlabel('False Positive Rate', fontsize=12)
ax.set_ylabel('True Positive Rate (Recall)', fontsize=12)
ax.set_title('Figure 11 — ROC Curves — All Models (Test Set)', fontweight='bold', fontsize=13)
ax.legend(loc='lower right', fontsize=10); sns.despine(); save('fig11_roc_curves.png')

# ── Figure 12: Metric comparison bar chart ────────────────────────────────────
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
metrics_list = ['Accuracy','Precision','Recall','F1 Score','ROC-AUC']
results = {}
for name in model_names:
    yp = trained[name].predict(X_test)
    ypr = trained[name].predict_proba(X_test)[:,1]
    results[name] = [accuracy_score(y_test,yp), precision_score(y_test,yp,zero_division=0),
                     recall_score(y_test,yp), f1_score(y_test,yp), roc_auc_score(y_test,ypr)]
x = np.arange(len(metrics_list)); bw = 0.18
colors4 = ['#4c72b0','#dd8452','#55a868','#c44e52']
fig, ax = plt.subplots(figsize=(13, 5))
for i,(name,color) in enumerate(zip(model_names,colors4)):
    off = x + (i-(len(model_names)-1)/2)*bw
    bars = ax.bar(off, results[name], width=bw, color=color, edgecolor='white', label=name)
    for bar,v in zip(bars,results[name]):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.005,
                f'{v:.3f}', ha='center', va='bottom', fontsize=7.5, rotation=90)
ax.set_xticks(x); ax.set_xticklabels(metrics_list, fontsize=11)
ax.set_ylabel('Score', fontsize=12); ax.set_ylim(0, 1.16)
ax.set_title('Figure 12 — Metric Comparison — All Models (Test Set)', fontweight='bold', fontsize=13)
ax.legend(title='Model', loc='upper left'); ax.axhline(y=0.5, color='grey', linestyle=':', linewidth=1)
sns.despine(); save('fig12_metric_comparison.png')

# ── Figure 13: LR Coefficients ───────────────────────────────────────────────
all_feature_names = model_arts['all_feature_names']
lr_clf = trained['Logistic Regression'].named_steps['classifier']
coef = lr_clf.coef_[0]
coef_df = pd.DataFrame({'Feature':all_feature_names,'Coefficient':coef,
                         'Abs':np.abs(coef)}).sort_values('Abs',ascending=False).head(20)
coef_df = coef_df.sort_values('Coefficient')
colors_lr = ['#dd8452' if v > 0 else '#4c72b0' for v in coef_df['Coefficient']]
fig, ax = plt.subplots(figsize=(9, 7))
ax.barh(coef_df['Feature'], coef_df['Coefficient'], color=colors_lr, edgecolor='white', height=0.7)
ax.axvline(x=0, color='black', linewidth=0.8)
ax.set_xlabel('Coefficient Value (log-odds scale)', fontsize=11)
ax.set_title('Figure 13 — Logistic Regression: Top 20 Feature Coefficients\n'
             '(orange = associated with higher churn log-odds; blue = lower)',
             fontweight='bold', fontsize=11)
for bar in ax.patches:
    w = bar.get_width()
    ax.text(w+(0.02 if w>=0 else -0.02), bar.get_y()+bar.get_height()/2,
            f'{w:+.3f}', va='center', ha='left' if w>=0 else 'right', fontsize=8.5)
sns.despine(); save('fig13_lr_coefficients.png')

# ── Figure 14: RF Feature Importances ────────────────────────────────────────
rf_clf = trained['Random Forest'].named_steps['classifier']
imp_df = pd.DataFrame({'Feature':all_feature_names,'Importance':rf_clf.feature_importances_})
top15 = imp_df.nlargest(15,'Importance').sort_values('Importance')
num_f = model_arts['numerical_features']
cat_f = model_arts['categorical_features']
def agg_imp(imp_df, num_f, cat_f):
    agg = {}
    for f in num_f: agg[f] = imp_df.loc[imp_df['Feature']==f,'Importance'].sum()
    for f in cat_f: agg[f] = imp_df.loc[imp_df['Feature'].str.startswith(f+'_'),'Importance'].sum()
    return pd.Series(agg).sort_values(ascending=False)
rf_agg = agg_imp(imp_df, num_f, cat_f)
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
axes[0].barh(top15['Feature'], top15['Importance'], color='#55a868', edgecolor='white', height=0.7)
for bar in axes[0].patches:
    axes[0].text(bar.get_width()+0.0002, bar.get_y()+bar.get_height()/2,
                 f'{bar.get_width():.4f}', va='center', fontsize=8.5)
axes[0].set_xlabel('Gini Importance')
axes[0].set_title('RF — Top 15 (OHE Columns)', fontweight='bold')
rf_agg_plot = rf_agg.sort_values().tail(12)
axes[1].barh(rf_agg_plot.index, rf_agg_plot.values, color='#4c72b0', edgecolor='white', height=0.7)
for bar in axes[1].patches:
    axes[1].text(bar.get_width()+0.0005, bar.get_y()+bar.get_height()/2,
                 f'{bar.get_width():.4f}', va='center', fontsize=8.5)
axes[1].set_xlabel('Gini Importance (aggregated)')
axes[1].set_title('RF — Aggregated by Original Feature', fontweight='bold')
plt.suptitle('Figure 14 — Random Forest Feature Importances', y=1.02, fontsize=13, fontweight='bold')
sns.despine(); save('fig14_rf_feature_importance.png')

# ── Figure 15: GB Feature Importances ────────────────────────────────────────
gb_clf = trained['Gradient Boosting'].named_steps['classifier']
gb_imp = pd.DataFrame({'Feature':all_feature_names,'Importance':gb_clf.feature_importances_})
top15_gb = gb_imp.nlargest(15,'Importance').sort_values('Importance')
gb_agg = agg_imp(gb_imp, num_f, cat_f)
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
axes[0].barh(top15_gb['Feature'], top15_gb['Importance'], color='#c44e52', edgecolor='white', height=0.7)
for bar in axes[0].patches:
    axes[0].text(bar.get_width()+0.0002, bar.get_y()+bar.get_height()/2,
                 f'{bar.get_width():.4f}', va='center', fontsize=8.5)
axes[0].set_xlabel('Gini Importance')
axes[0].set_title('GB — Top 15 (OHE Columns)', fontweight='bold')
gb_agg_plot = gb_agg.sort_values().tail(12)
axes[1].barh(gb_agg_plot.index, gb_agg_plot.values, color='#dd8452', edgecolor='white', height=0.7)
for bar in axes[1].patches:
    axes[1].text(bar.get_width()+0.0005, bar.get_y()+bar.get_height()/2,
                 f'{bar.get_width():.4f}', va='center', fontsize=8.5)
axes[1].set_xlabel('Gini Importance (aggregated)')
axes[1].set_title('GB — Aggregated by Original Feature', fontweight='bold')
plt.suptitle('Figure 15 — Gradient Boosting Feature Importances', y=1.02, fontsize=13, fontweight='bold')
sns.despine(); save('fig15_gb_feature_importance.png')

print('\nAll figures rendered successfully.')
