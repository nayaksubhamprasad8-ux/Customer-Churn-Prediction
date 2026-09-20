"""
Build report/Subham_Customer_Churn_Project_Report.docx using python-docx.
Runs from the project root or report/ directory.
All metrics are sourced from Step 7 executed output cells.
"""
import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
FIG_DIR      = os.path.join(SCRIPT_DIR, 'figures')
OUT_PATH     = os.path.join(SCRIPT_DIR, 'Subham_Customer_Churn_Project_Report.docx')

def fig(name):
    return os.path.join(FIG_DIR, name)

# ── Helpers ───────────────────────────────────────────────────────────────────
def add_page_number(doc):
    """Add 'Page X of Y' footer to every section."""
    section = doc.sections[0]
    footer  = section.footer
    para    = footer.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.clear()
    run = para.add_run('Page ')
    fldChar = OxmlElement('w:fldChar'); fldChar.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText'); instrText.text = 'PAGE'
    fldChar2 = OxmlElement('w:fldChar'); fldChar2.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar); run._r.append(instrText); run._r.append(fldChar2)
    para.add_run(' of ')
    run2 = para.add_run()
    fldChar3 = OxmlElement('w:fldChar'); fldChar3.set(qn('w:fldCharType'), 'begin')
    instrText2 = OxmlElement('w:instrText'); instrText2.text = 'NUMPAGES'
    fldChar4 = OxmlElement('w:fldChar'); fldChar4.set(qn('w:fldCharType'), 'end')
    run2._r.append(fldChar3); run2._r.append(instrText2); run2._r.append(fldChar4)
    for run in para.runs:
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x60, 0x60, 0x60)

def set_cell_bg(cell, hex_color):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  hex_color)
    tcPr.append(shd)

def style_table(table, header_bg='1F4E79', header_fg='FFFFFF', col_widths=None):
    """Apply professional table styling."""
    table.style = 'Table Grid'
    for i, row in enumerate(table.rows):
        for j, cell in enumerate(row.cells):
            for para in cell.paragraphs:
                for run in para.runs:
                    run.font.size = Pt(10)
                    if i == 0:
                        run.font.bold  = True
                        run.font.color.rgb = RGBColor(
                            int(header_fg[0:2],16), int(header_fg[2:4],16), int(header_fg[4:6],16))
            if i == 0:
                set_cell_bg(cell, header_bg)
    if col_widths:
        for row in table.rows:
            for j, cell in enumerate(row.cells):
                if j < len(col_widths):
                    cell.width = col_widths[j]

def add_heading(doc, text, level):
    heading = doc.add_heading(text, level=level)
    heading.style.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    return heading

def add_body(doc, text, space_after=6):
    para = doc.add_paragraph(text)
    para.style = doc.styles['Normal']
    para.paragraph_format.space_after = Pt(space_after)
    para.paragraph_format.space_before = Pt(0)
    for run in para.runs:
        run.font.size  = Pt(11)
        run.font.name  = 'Calibri'
    return para

def add_caption(doc, text):
    para = doc.add_paragraph(text)
    para.paragraph_format.space_before = Pt(3)
    para.paragraph_format.space_after  = Pt(10)
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in para.runs:
        run.font.size   = Pt(9)
        run.font.italic = True
        run.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

def add_figure(doc, filename, width_inches, caption_text):
    if not os.path.exists(fig(filename)):
        add_body(doc, f'[Figure not found: {filename}]')
        return
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(8)
    para.paragraph_format.space_after  = Pt(2)
    run = para.add_run()
    run.add_picture(fig(filename), width=Inches(width_inches))
    add_caption(doc, caption_text)

def bullet(doc, text):
    para = doc.add_paragraph(text, style='List Bullet')
    para.paragraph_format.space_after  = Pt(3)
    para.paragraph_format.space_before = Pt(0)
    for run in para.runs:
        run.font.size = Pt(11)

# ── Build document ────────────────────────────────────────────────────────────
doc = Document()

# ── Page margins ──────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin   = Cm(2.54)
    section.right_margin  = Cm(2.54)
    section.different_first_page_header_footer = False

# ── Default Normal font ───────────────────────────────────────────────────────
normal = doc.styles['Normal']
normal.font.name = 'Calibri'
normal.font.size = Pt(11)

# ── Heading styles ────────────────────────────────────────────────────────────
for style_name, pt_size in [('Heading 1', 16), ('Heading 2', 13), ('Heading 3', 11)]:
    st = doc.styles[style_name]
    st.font.name  = 'Calibri'
    st.font.size  = Pt(pt_size)
    st.font.bold  = True
    st.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    st.paragraph_format.space_before = Pt(14)
    st.paragraph_format.space_after  = Pt(4)

# ═══════════════════════════════════════════════════════════════════════════════
# TITLE PAGE
# ═══════════════════════════════════════════════════════════════════════════════
for _ in range(4):
    doc.add_paragraph()

title_para = doc.add_paragraph()
title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_run = title_para.add_run('Customer Churn Prediction\nUsing Machine Learning')
title_run.font.name  = 'Calibri'
title_run.font.size  = Pt(26)
title_run.font.bold  = True
title_run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
title_para.paragraph_format.space_after = Pt(30)

for text, size, bold in [
    ('Subham', 16, True),
    ('Internship Project Report', 13, False),
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.font.name = 'Calibri'; r.font.size = Pt(size); r.font.bold = bold
    p.paragraph_format.space_after = Pt(6)

doc.add_paragraph()

# Title page details table
tbl = doc.add_table(rows=5, cols=2)
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl.style = 'Table Grid'
details = [
    ('Organization / Company', '____________________'),
    ('Internship Duration',    '____________________'),
    ('Mentor / Supervisor',    '____________________'),
    ('Submission Date',        '____________________'),
    ('Student Name',           'Subham'),
]
for row, (label, value) in zip(tbl.rows, details):
    lc = row.cells[0]; vc = row.cells[1]
    lc.width = Inches(2.2); vc.width = Inches(3.5)
    lr = lc.paragraphs[0].add_run(label)
    lr.font.bold = True; lr.font.size = Pt(11)
    vr = vc.paragraphs[0].add_run(value)
    vr.font.size = Pt(11)
    set_cell_bg(lc, 'D9E1F2')

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# TABLE OF CONTENTS (field-based — updates on F9 in Word)
# ═══════════════════════════════════════════════════════════════════════════════
toc_heading = doc.add_paragraph('Table of Contents')
toc_heading.style = doc.styles['Heading 1']
toc_heading.paragraph_format.space_before = Pt(0)

toc_para = doc.add_paragraph()
toc_fld  = OxmlElement('w:fldChar'); toc_fld.set(qn('w:fldCharType'), 'begin')
toc_instr = OxmlElement('w:instrText')
toc_instr.set(qn('xml:space'), 'preserve')
toc_instr.text = 'TOC \\o "1-3" \\h \\z \\u'
toc_end  = OxmlElement('w:fldChar'); toc_end.set(qn('w:fldCharType'), 'end')
run = toc_para.add_run()
run._r.append(toc_fld); run._r.append(toc_instr); run._r.append(toc_end)
toc_para.paragraph_format.space_after = Pt(6)

doc.add_paragraph('(Press Ctrl+A then F9 in Microsoft Word to update the Table of Contents.)',
                   style='Normal').runs[0].font.italic = True

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 1. ABSTRACT
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('1. Abstract', 1)
add_body(doc, 'Customer churn — the voluntary cancellation of a service subscription — represents a significant revenue risk in the telecommunications industry. This project develops a machine learning pipeline to predict whether a telecom customer is likely to churn, using demographic, service subscription, contract, and billing data from 7,043 customer records sourced from the publicly available Telco Customer Churn dataset (Kaggle / IBM Watson Analytics).')
add_body(doc, 'Four binary classification models were trained and evaluated on a held-out test set of 1,405 rows: Logistic Regression, Decision Tree, Random Forest, and Gradient Boosting. All preprocessing — including standard scaling and one-hot encoding — was encapsulated within scikit-learn Pipeline objects to prevent data leakage. Models were compared using Accuracy, Precision, Recall, F1-Score, and ROC-AUC on the positive class (Churn = 1).')
add_body(doc, 'Random Forest was selected as the final model on the basis of its highest F1-Score (0.6168), competitive ROC-AUC (0.8372), and the most balanced profile between Precision (0.5520) and Recall (0.6989). The final pipeline is saved to disk and demonstrated on synthetic new customer records. All findings are presented as statistical associations; no causal claims are made.', space_after=12)

# ═══════════════════════════════════════════════════════════════════════════════
# 2. INTRODUCTION
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('2. Introduction', 1)
add_body(doc, 'Customer retention is a strategic priority for telecommunications providers. Industry evidence consistently shows that the cost of acquiring a new customer substantially exceeds the cost of retaining an existing one. Churn — when a customer discontinues their subscription — not only represents direct revenue loss but also signals dissatisfaction that can influence other customers.')
add_body(doc, 'Predictive modelling offers a proactive approach: by identifying customers who show a statistical profile similar to those who have churned historically, a business can prioritise retention interventions such as personalised offers or service reviews before the customer leaves. Machine learning is well-suited to this problem because churn is influenced by a combination of factors — tenure, contract type, service bundles, billing method, and demographics — whose interactions are difficult to capture with simple rules.')
add_body(doc, 'This project implements a complete, reproducible end-to-end pipeline across nine structured Jupyter notebooks, progressing from data quality audit and cleaning through exploratory analysis, preprocessing, model training, evaluation, interpretation, and final inference on new customer records.', space_after=12)

# ═══════════════════════════════════════════════════════════════════════════════
# 3. PROBLEM STATEMENT
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('3. Problem Statement', 1)
add_body(doc, 'Task type: Binary classification — predict whether a customer will churn (positive class = 1) or remain (negative class = 0).')
add_body(doc, 'Input: A set of 19 feature columns describing each customer\'s demographic characteristics, service subscriptions, account configuration, and billing information.')
add_body(doc, 'Output: A predicted label — Churn (1) or No Churn (0) — and an associated probability score representing the model\'s estimated likelihood that the customer will churn.')
add_body(doc, 'The class distribution is moderately imbalanced: approximately 73.6% of customers did not churn and 26.4% did. A naive model predicting "No Churn" for every customer would achieve approximately 73.6% accuracy while identifying zero churners — illustrating why accuracy alone is an insufficient metric for this problem.', space_after=12)

# ═══════════════════════════════════════════════════════════════════════════════
# 4. OBJECTIVES
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('4. Objectives', 1)
for obj in [
    'Conduct a systematic data quality audit to identify and document all data issues before modelling.',
    'Clean the dataset and record the rationale behind every cleaning decision.',
    'Perform exploratory data analysis (EDA) to understand feature distributions and their associations with churn.',
    'Build a leakage-free preprocessing pipeline using scikit-learn Pipeline and ColumnTransformer.',
    'Train four baseline classification models using consistent preprocessing and reproducible hyperparameters.',
    'Evaluate all models on a held-out test set using metrics appropriate for imbalanced classification.',
    'Interpret model outputs through coefficient analysis and feature importances.',
    'Select and document the final model using transparent, criteria-driven reasoning.',
    'Demonstrate inference on new, unseen hypothetical customer records using the saved final pipeline.',
]:
    bullet(doc, obj)
doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════════════════════
# 5. DATASET DESCRIPTION
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('5. Dataset Description', 1)
add_body(doc, 'The project uses the Telco Customer Churn dataset, a publicly available dataset from Kaggle (originally published as part of IBM Watson Analytics sample data). It represents a snapshot of 7,043 customers of a fictional telecommunications provider.')

# Dataset overview table
tbl = doc.add_table(rows=6, cols=2)
tbl.style = 'Table Grid'; tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
rows_data = [
    ('Property', 'Value', True),
    ('Dataset Name', 'Telco Customer Churn', False),
    ('Source', 'Kaggle / IBM Watson Analytics Sample Data', False),
    ('Raw Records', '7,043 rows × 21 columns', False),
    ('Records After Cleaning', '7,021 rows × 20 columns', False),
    ('Target Variable', 'Churn (Yes / No — encoded as 1 / 0)', False),
]
for i, (r) in enumerate(tbl.rows):
    label, value, is_header = rows_data[i]
    lc = r.cells[0]; vc = r.cells[1]
    lc.width = Inches(2.5); vc.width = Inches(4.0)
    lr = lc.paragraphs[0].add_run(label)
    vr = vc.paragraphs[0].add_run(value)
    for run in [lr, vr]:
        run.font.size = Pt(10)
        run.font.bold = is_header
    if is_header:
        set_cell_bg(lc, '1F4E79'); set_cell_bg(vc, '1F4E79')
        for run in [lr, vr]: run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    elif i % 2 == 0:
        set_cell_bg(lc, 'EBF0F7'); set_cell_bg(vc, 'EBF0F7')
doc.add_paragraph()

doc.add_heading('5.1 Feature Descriptions', 2)
feat_data = [
    ('Feature', 'Data Type', 'Description', True),
    ('gender', 'Categorical', 'Customer gender: Male or Female', False),
    ('SeniorCitizen', 'Numeric (0/1)', 'Whether the customer is a senior citizen (1 = yes, 0 = no)', False),
    ('Partner', 'Categorical', 'Whether the customer has a partner: Yes or No', False),
    ('Dependents', 'Categorical', 'Whether the customer has dependents: Yes or No', False),
    ('tenure', 'Numeric (integer)', 'Months the customer has been with the company (0–72)', False),
    ('PhoneService', 'Categorical', 'Whether the customer has phone service: Yes or No', False),
    ('MultipleLines', 'Categorical', 'Multiple phone lines: Yes, No, or No phone service', False),
    ('InternetService', 'Categorical', 'Internet service type: DSL, Fiber optic, or No', False),
    ('OnlineSecurity', 'Categorical', 'Online security add-on: Yes, No, or No internet service', False),
    ('OnlineBackup', 'Categorical', 'Online backup add-on: Yes, No, or No internet service', False),
    ('DeviceProtection', 'Categorical', 'Device protection add-on: Yes, No, or No internet service', False),
    ('TechSupport', 'Categorical', 'Tech support add-on: Yes, No, or No internet service', False),
    ('StreamingTV', 'Categorical', 'TV streaming: Yes, No, or No internet service', False),
    ('StreamingMovies', 'Categorical', 'Movie streaming: Yes, No, or No internet service', False),
    ('Contract', 'Categorical', 'Contract term: Month-to-month, One year, or Two year', False),
    ('PaperlessBilling', 'Categorical', 'Whether the customer uses paperless billing: Yes or No', False),
    ('PaymentMethod', 'Categorical', 'Payment method: Electronic check, Mailed check, Bank transfer (automatic), or Credit card (automatic)', False),
    ('MonthlyCharges', 'Numeric (float)', 'Monthly amount charged to the customer (USD)', False),
    ('TotalCharges', 'Numeric (float)', 'Total amount charged over tenure; converted from string dtype in cleaning', False),
    ('Churn', 'Binary target', 'Whether the customer churned: Yes (1) or No (0)', False),
]
tbl2 = doc.add_table(rows=len(feat_data), cols=3)
tbl2.style = 'Table Grid'; tbl2.alignment = WD_TABLE_ALIGNMENT.LEFT
for i, row in enumerate(tbl2.rows):
    feat, dtype, desc, is_header = feat_data[i]
    row.cells[0].width = Inches(1.5)
    row.cells[1].width = Inches(1.5)
    row.cells[2].width = Inches(3.5)
    for j, (cell, txt) in enumerate(zip(row.cells, [feat, dtype, desc])):
        r = cell.paragraphs[0].add_run(txt)
        r.font.size = Pt(9.5)
        r.font.bold = is_header
        if is_header:
            set_cell_bg(cell, '1F4E79')
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        elif i % 2 == 0:
            set_cell_bg(cell, 'F2F5FA')
doc.add_paragraph()

doc.add_heading('5.2 Class Distribution', 2)
add_body(doc, 'The target variable Churn is moderately imbalanced, with approximately 73.6% of customers not churning and 26.4% churning. This 3:1 ratio is accounted for through class weighting in model configuration and through the use of metrics (F1, ROC-AUC) that are more appropriate than accuracy for imbalanced classification.')
tbl3 = doc.add_table(rows=3, cols=3)
tbl3.style = 'Table Grid'; tbl3.alignment = WD_TABLE_ALIGNMENT.LEFT
for i, row in enumerate(tbl3.rows):
    row_data = [('Class', 'Count', 'Percentage'),
                ('No Churn (0)', '5,164', '73.6%'),
                ('Churn (1)', '1,857', '26.4%')][i]
    for j, (cell, txt) in enumerate(zip(row.cells, row_data)):
        r = cell.paragraphs[0].add_run(txt)
        r.font.size = Pt(10)
        r.font.bold = (i == 0)
        if i == 0: set_cell_bg(cell, '1F4E79'); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════════════════════
# 6. TOOLS AND TECHNOLOGIES
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('6. Tools and Technologies', 1)
add_body(doc, 'The following Python packages were used throughout the project. All version numbers reflect the development environment.')
tech_data = [
    ('Category', 'Package', 'Version', 'Role', True),
    ('Language', 'Python', '3.12', 'All notebooks and pipeline code', False),
    ('Data manipulation', 'pandas', '2.3.3', 'Loading, cleaning, transforming, and analysing tabular data', False),
    ('Numerical computation', 'NumPy', '1.26.4', 'Array operations, coefficient extraction, importance arrays', False),
    ('Visualisation', 'Matplotlib', '3.10.8', 'All plots including histograms, bar charts, and ROC curves', False),
    ('Visualisation', 'seaborn', '0.13.2', 'Statistical plots, heatmaps, KDE overlays, theme styling', False),
    ('Machine learning', 'scikit-learn', '1.4.1', 'Pipelines, preprocessing, models, and all evaluation metrics', False),
    ('ML dependency', 'SciPy', '1.17.0', 'Required by scikit-learn solvers and internal computations', False),
    ('Model serialisation', 'joblib', '1.5.3', 'Saving and loading trained pipelines and data splits', False),
    ('Notebook environment', 'Jupyter Notebook', '7.6.1', 'Interactive execution of all nine project notebooks', False),
    ('Kernel', 'ipykernel', '7.2.0', 'Python kernel for Jupyter cell execution', False),
]
tbl4 = doc.add_table(rows=len(tech_data), cols=4)
tbl4.style = 'Table Grid'; tbl4.alignment = WD_TABLE_ALIGNMENT.LEFT
for i, row in enumerate(tbl4.rows):
    cat, pkg, ver, role, is_header = tech_data[i]
    row.cells[0].width = Inches(1.5)
    row.cells[1].width = Inches(1.3)
    row.cells[2].width = Inches(0.8)
    row.cells[3].width = Inches(3.0)
    for j, (cell, txt) in enumerate(zip(row.cells, [cat, pkg, ver, role])):
        r = cell.paragraphs[0].add_run(txt)
        r.font.size = Pt(9.5); r.font.bold = is_header
        if is_header: set_cell_bg(cell, '1F4E79'); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        elif i % 2 == 0: set_cell_bg(cell, 'F2F5FA')
doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════════════════════
# 7. DATA QUALITY ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('7. Data Quality Analysis', 1)
add_body(doc, 'A systematic data quality audit was performed on the raw CSV before any cleaning or modelling. The following issues were identified.')

doc.add_heading('7.1 Dataset Shape', 2)
add_body(doc, 'The raw dataset contains 7,043 rows and 21 columns, including customerID (an administrative identifier) and the target column Churn.')

doc.add_heading('7.2 Duplicate Records', 2)
add_body(doc, 'A complete row-level deduplication check found zero duplicate rows. No rows were removed for duplication.')

doc.add_heading('7.3 Missing Values', 2)
add_body(doc, 'Pandas .isnull().sum() returned zero missing values across all columns. However, this result was misleading for one column.')

doc.add_heading('7.4 TotalCharges — Hidden Blank Strings', 2)
add_body(doc, 'TotalCharges was stored as object dtype (string) despite containing numeric values. A secondary check for blank or whitespace-only strings revealed 11 rows in which TotalCharges was an empty string — a form of missing data that pandas standard NaN detection does not flag. All 11 affected rows had tenure = 0.')

dq_tbl_data = [
    ('Check', 'Finding', True),
    ('TotalCharges dtype', 'object (string) — should be float64', False),
    ('Rows with blank TotalCharges', '11', False),
    ('tenure value for all 11 blank rows', '0 (customers in first billing period)', False),
]
tbl5 = doc.add_table(rows=len(dq_tbl_data), cols=2)
tbl5.style = 'Table Grid'
for i, row in enumerate(tbl5.rows):
    check, finding, is_header = dq_tbl_data[i]
    row.cells[0].width = Inches(3.0); row.cells[1].width = Inches(3.5)
    for cell, txt in zip(row.cells, [check, finding]):
        r = cell.paragraphs[0].add_run(txt)
        r.font.size = Pt(10); r.font.bold = is_header
        if is_header: set_cell_bg(cell, '1F4E79'); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
doc.add_paragraph()

doc.add_heading('7.5 customerID Column', 2)
add_body(doc, 'customerID is a unique administrative identifier (7,043 unique values, one per row). It carries no predictive information and was flagged for removal.')

doc.add_heading('7.6 Class Distribution', 2)
add_body(doc, 'The target variable Churn has a moderately imbalanced distribution in the raw dataset: approximately 73.5% No Churn and 26.5% Churn. This imbalance is addressed through class weighting in model configuration and appropriate metric selection during evaluation.', space_after=12)

# ═══════════════════════════════════════════════════════════════════════════════
# 8. DATA CLEANING
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('8. Data Cleaning', 1)
add_body(doc, 'All cleaning operations were applied to a copy of the raw DataFrame. The raw CSV was never modified. The following operations were performed.')

cleaning_data = [
    ('Operation', 'Action', 'Rationale', True),
    ('Remove customerID', 'Dropped the customerID column', 'Arbitrary identifier with no predictive value; including it could cause tree-based models to memorise training rows', False),
    ('Convert TotalCharges dtype', 'Applied pd.to_numeric(..., errors="coerce") to convert from object to float64', 'Column contains numeric values stored as strings due to the 11 blank entries', False),
    ('Impute blank TotalCharges', 'Filled 11 resulting NaN values with 0.0', 'All 11 rows had tenure = 0 — customers had not completed a billing cycle; zero is factually correct', False),
    ('Retain SeniorCitizen as int', 'No action', 'Already a clean binary indicator (0/1); round-tripping to string would be unnecessary', False),
    ('Service category values', 'No modification', '"No internet service" is a valid category, not a missing-value indicator; replacing it with NaN would be incorrect', False),
]
tbl6 = doc.add_table(rows=len(cleaning_data), cols=3)
tbl6.style = 'Table Grid'
for i, row in enumerate(tbl6.rows):
    op, action, rat, is_header = cleaning_data[i]
    row.cells[0].width = Inches(1.5); row.cells[1].width = Inches(2.5); row.cells[2].width = Inches(2.5)
    for cell, txt in zip(row.cells, [op, action, rat]):
        r = cell.paragraphs[0].add_run(txt)
        r.font.size = Pt(9.5); r.font.bold = is_header
        if is_header: set_cell_bg(cell, '1F4E79'); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        elif i % 2 == 0: set_cell_bg(cell, 'F2F5FA')
doc.add_paragraph()

add_body(doc, 'After cleaning: 7,021 rows × 20 columns, zero missing values.', space_after=12)

# ═══════════════════════════════════════════════════════════════════════════════
# 9. EXPLORATORY DATA ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
doc.add_heading('9. Exploratory Data Analysis', 1)
add_body(doc, 'All findings in this section are stated as associations observed in the dataset. They do not imply causal relationships between features and churn.')

doc.add_heading('9.1 Target Variable Distribution', 2)
add_body(doc, 'The target class is moderately imbalanced at approximately 3:1. A naive model predicting "No Churn" for every customer would achieve ~73.6% accuracy without learning any pattern — illustrating why accuracy alone is insufficient for this dataset.')
add_figure(doc, 'fig01_churn_distribution.png', 5.5,
           'Figure 1 — Churn Class Distribution. 73.6% No Churn vs 26.4% Churn (N = 7,021).')

doc.add_heading('9.2 Numerical Feature Distributions', 2)
add_body(doc, 'tenure is bimodal — many customers are either very new (0–5 months) or long-tenured (50–72 months). MonthlyCharges is right-skewed with a cluster around $20. TotalCharges is heavily right-skewed, closely related to tenure × MonthlyCharges.')
add_figure(doc, 'fig02_numerical_distributions.png', 6.2,
           'Figure 2 — Overall distributions of tenure, MonthlyCharges, and TotalCharges.')
add_figure(doc, 'fig03_numerical_by_churn.png', 6.2,
           'Figure 3 — Numerical feature distributions split by Churn status. Churned customers have shorter tenure and higher monthly charges on average.')

doc.add_heading('9.3 Churn Rate by Contract Type', 2)
add_body(doc, 'Contract type shows the largest churn rate gap of any single categorical feature. Month-to-month customers churn at approximately 43%, compared to 11% for one-year and 3% for two-year contracts.')
add_figure(doc, 'fig04_churn_by_contract.png', 5.5,
           'Figure 4 — Churn Rate by Contract Type. Month-to-month customers show a churn rate more than four times the dataset average.')

doc.add_heading('9.4 Churn Rate by Tenure', 2)
add_body(doc, 'Churn risk is highest in the first year (~48%) and declines monotonically with increasing tenure to below 10% for customers with 61–72 months tenure.')
add_figure(doc, 'fig05_churn_by_tenure.png', 5.8,
           'Figure 5 — Churn Rate by Tenure Bucket. The rate declines sharply with increasing tenure.')

doc.add_heading('9.5 Churn Rate by Internet Service Type', 2)
add_body(doc, 'Fibre optic customers churn at approximately 42% — more than double the rate of DSL customers (~19%) and six times the rate of customers with no internet service (~7%).')
add_figure(doc, 'fig06_churn_by_internet.png', 5.5,
           'Figure 6 — Churn Rate by Internet Service Type. Fibre optic customers show the highest churn rate.')

doc.add_heading('9.6 Churn Rate by Add-On Services', 2)
add_body(doc, 'Across Tech Support, Online Security, Online Backup, and Device Protection, customers without add-on subscriptions show churn rates of 40–42%, compared to 14–16% for subscribers.')
add_figure(doc, 'fig07_churn_by_addons.png', 6.0,
           'Figure 7 — Churn Rate by Tech Support and Online Security. Customers without add-on services show substantially higher churn rates.')

doc.add_heading('9.7 Churn Rate by Payment Method', 2)
add_body(doc, 'Electronic check payers churn at approximately 45% — nearly three times the rate of customers on automatic payment methods (16–18%).')
add_figure(doc, 'fig08_churn_by_payment.png', 6.0,
           'Figure 8 — Churn Rate by Payment Method. Electronic check payers show the highest churn rate.')

doc.add_heading('9.8 Correlation Analysis', 2)
add_body(doc, 'tenure and TotalCharges are strongly correlated (r = +0.83), signalling potential multicollinearity. tenure shows a moderate negative correlation with Churn (r = −0.35). MonthlyCharges shows a weak positive correlation (r = +0.19).')
add_figure(doc, 'fig09_correlation_heatmap.png', 5.0,
           'Figure 9 — Pearson Correlation Heatmap. Strong correlation between tenure and TotalCharges (r = 0.83) indicates potential multicollinearity.')
doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════════════════════
# 10. FEATURE ENGINEERING AND PREPROCESSING
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('10. Feature Engineering and Preprocessing', 1)

doc.add_heading('10.1 Target Encoding', 2)
add_body(doc, 'The target column Churn (string: "Yes"/"No") was encoded as binary integer: "No" → 0 (retained), "Yes" → 1 (churned). This is the standard expectation of scikit-learn classifiers.')

doc.add_heading('10.2 Train / Test Split', 2)
split_data = [
    ('Parameter', 'Value', 'Rationale', True),
    ('test_size', '0.20', '80/20 split; 1,405 test rows provides reliable metric estimates', False),
    ('random_state', '42', 'Full reproducibility across runs', False),
    ('stratify', 'y', 'Preserves 73.6/26.4 class ratio in both partitions', False),
    ('Training rows', '5,616', '', False),
    ('Test rows', '1,405', '', False),
]
tbl7 = doc.add_table(rows=len(split_data), cols=3)
tbl7.style = 'Table Grid'
for i, row in enumerate(tbl7.rows):
    param, val, rat, is_header = split_data[i]
    row.cells[0].width = Inches(1.5); row.cells[1].width = Inches(1.0); row.cells[2].width = Inches(4.0)
    for cell, txt in zip(row.cells, [param, val, rat]):
        r = cell.paragraphs[0].add_run(txt)
        r.font.size = Pt(10); r.font.bold = is_header
        if is_header: set_cell_bg(cell, '1F4E79'); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
doc.add_paragraph()

doc.add_heading('10.3 Preprocessing Pipeline', 2)
add_body(doc, 'All preprocessing is encapsulated inside a scikit-learn ColumnTransformer, which is the first step of each model Pipeline. This ensures preprocessing is applied consistently before every prediction.')
add_body(doc, 'Numerical pipeline (4 features: SeniorCitizen, tenure, MonthlyCharges, TotalCharges): SimpleImputer (strategy="median") → StandardScaler. The scaler centres each feature at zero and scales to unit variance, which is required for distance-sensitive models.')
add_body(doc, 'Categorical pipeline (15 features): SimpleImputer (strategy="most_frequent") → OneHotEncoder (handle_unknown="ignore", sparse_output=False). One-hot encoding is used instead of ordinal integer encoding because all 15 categorical features are nominal — assigning integers would impose false ordinal relationships.')
add_body(doc, 'The ColumnTransformer produces 45 output features: 4 scaled numerical + 41 one-hot encoded columns.')

doc.add_heading('10.4 Prevention of Data Leakage', 2)
add_body(doc, 'The train/test split is performed before any preprocessing is fitted. Each model Pipeline calls .fit(X_train, y_train), which fits the scaler and encoder exclusively on training data. Calling .predict(X_test) then applies the already-fitted parameters to the test set — the test set never influences the transformation parameters.', space_after=12)

# ═══════════════════════════════════════════════════════════════════════════════
# 11. MACHINE LEARNING METHODOLOGY
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('11. Machine Learning Methodology', 1)
add_body(doc, 'Four binary classification models were trained. Each is wrapped in a Pipeline(preprocessor → classifier), ensuring consistent preprocessing and preventing leakage. All models use random_state=42 for reproducibility.')

doc.add_heading('11.1 Logistic Regression', 2)
add_body(doc, 'A linear probabilistic classifier that models the log-odds of churn as a weighted sum of scaled input features. Provides interpretable coefficients and serves as the linear baseline. Configured with C=1.0, max_iter=1000, class_weight="balanced" (to compensate for the 73.6/26.4 imbalance), solver=lbfgs.')

doc.add_heading('11.2 Decision Tree Classifier', 2)
add_body(doc, 'A non-linear model that learns axis-aligned decision rules through recursive binary splitting on individual features. Without depth constraints a single tree memorises the training set. Configured with max_depth=10, min_samples_leaf=20, class_weight="balanced".')

doc.add_heading('11.3 Random Forest Classifier', 2)
add_body(doc, 'An ensemble of 200 independently trained decision trees, each fitted on a bootstrap sample with a random feature subset at each split. Aggregating over trees reduces variance substantially compared to a single tree. Configured with n_estimators=200, min_samples_leaf=5, class_weight="balanced_subsample", n_jobs=-1.')

doc.add_heading('11.4 Gradient Boosting Classifier', 2)
add_body(doc, 'An ensemble that trains trees sequentially, each correcting the residual errors of the current model. Configured with n_estimators=200, learning_rate=0.1, max_depth=4, subsample=0.8. Does not support class_weight; the boosting mechanism provides partial compensation for class imbalance.')

doc.add_heading('11.5 Why Multiple Models Were Compared', 2)
add_body(doc, 'No single algorithm dominates on all tabular classification tasks. Logistic Regression provides an interpretable linear baseline; Decision Tree captures non-linearity; Random Forest and Gradient Boosting reduce variance/bias through ensembles. Comparing all four on the same held-out test set provides an evidence-based foundation for model selection rather than assuming one approach is superior.', space_after=12)

# ═══════════════════════════════════════════════════════════════════════════════
# 12. MODEL EVALUATION
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
doc.add_heading('12. Model Evaluation', 1)
add_body(doc, 'All evaluation metrics were computed on the held-out test set (1,405 rows, untouched during training). The positive class is Churn = 1.')

doc.add_heading('12.1 Metric Definitions', 2)
metric_def = [
    ('Metric', 'Formula', 'Interpretation in Churn Context', True),
    ('Accuracy', '(TP + TN) / N', 'Overall fraction correct; misleading when classes are imbalanced', False),
    ('Precision', 'TP / (TP + FP)', 'Of all customers predicted to churn, the fraction that actually did', False),
    ('Recall', 'TP / (TP + FN)', 'Of all customers who actually churned, the fraction the model identified', False),
    ('F1-Score', '2·(P·R) / (P+R)', 'Harmonic mean of Precision and Recall; high only when both are reasonable', False),
    ('ROC-AUC', 'Area under ROC curve', 'Probability that the model ranks a random churner above a random non-churner; threshold-independent', False),
]
tbl8 = doc.add_table(rows=len(metric_def), cols=3)
tbl8.style = 'Table Grid'
for i, row in enumerate(tbl8.rows):
    m, f, interp, is_header = metric_def[i]
    row.cells[0].width = Inches(1.3); row.cells[1].width = Inches(1.7); row.cells[2].width = Inches(3.5)
    for cell, txt in zip(row.cells, [m, f, interp]):
        r = cell.paragraphs[0].add_run(txt)
        r.font.size = Pt(9.5); r.font.bold = is_header
        if is_header: set_cell_bg(cell, '1F4E79'); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        elif i % 2 == 0: set_cell_bg(cell, 'F2F5FA')
doc.add_paragraph()

doc.add_heading('12.2 Results Table', 2)
add_body(doc, 'The following metrics were measured on the test set. Bold values indicate the highest score in each column.')
eval_data = [
    ('Model', 'Accuracy', 'Precision', 'Recall', 'F1 Score', 'ROC-AUC', True),
    ('Logistic Regression', '0.7416', '0.5079', '0.7796', '0.6151', '0.8398', False),
    ('Random Forest',       '0.7701', '0.5520', '0.6989', '0.6168', '0.8372', False),
    ('Gradient Boosting',   '0.7907', '0.6413', '0.4758', '0.5463', '0.8333', False),
    ('Decision Tree',       '0.7274', '0.4898', '0.7124', '0.5805', '0.8148', False),
]
# Best value per column (cols 1-5, rows 1-4): indices of best per metric
best = {1: 2, 2: 2, 3: 0, 4: 1, 5: 0}  # row index of best value per col
tbl9 = doc.add_table(rows=5, cols=6)
tbl9.style = 'Table Grid'
for i, row in enumerate(tbl9.rows):
    model, acc, prec, rec, f1, auc, is_header = eval_data[i]
    vals = [model, acc, prec, rec, f1, auc]
    for j, (cell, txt) in enumerate(zip(row.cells, vals)):
        r = cell.paragraphs[0].add_run(txt)
        r.font.size = Pt(10)
        r.font.bold = is_header or (not is_header and j > 0 and best.get(j) == i - 1)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
        if is_header: set_cell_bg(cell, '1F4E79'); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        elif i == 2: set_cell_bg(cell, 'E2EFDA')  # highlight RF row
doc.add_paragraph()
add_body(doc, 'The Random Forest row is highlighted as the selected final model.')

doc.add_heading('12.3 Confusion Matrices', 2)
add_body(doc, 'Each matrix shows TN / FP / FN / TP counts and row-normalised percentages. False Negatives (FN) — missed churners — are typically the most costly error in a retention context. Gradient Boosting has the highest FN rate (~52%), while Logistic Regression and Decision Tree have the lowest.')
add_figure(doc, 'fig10_confusion_matrices.png', 6.5,
           'Figure 10 — Confusion Matrices for all four models (test set, row-normalised). Cells show label, raw count, and row percentage.')

doc.add_heading('12.4 ROC Curves', 2)
add_body(doc, 'ROC-AUC measures the model\'s ability to rank churners above non-churners at all probability thresholds. All four models substantially outperform random classification (AUC = 0.50). The differences between Logistic Regression (0.8398), Random Forest (0.8372), and Gradient Boosting (0.8333) are small; model selection is better driven by precision–recall trade-offs.')
add_figure(doc, 'fig11_roc_curves.png', 5.5,
           'Figure 11 — ROC Curves for all four models (test set). Dashed diagonal line = random classifier baseline (AUC = 0.50).')

doc.add_heading('12.5 Metric Comparison', 2)
add_figure(doc, 'fig12_metric_comparison.png', 6.5,
           'Figure 12 — All five evaluation metrics compared across models (test set). Gradient Boosting has the highest accuracy and precision; Logistic Regression has the highest recall; Random Forest has the highest F1-Score.')

doc.add_heading('12.6 Why Accuracy Is Misleading Here', 2)
add_body(doc, 'A trivial model predicting "No Churn" for every customer would achieve approximately 73.6% accuracy on this test set — higher than Logistic Regression and Decision Tree — while having a Recall of 0 (identifying zero churners). This illustrates why Recall, F1-Score, and ROC-AUC are more informative for imbalanced classification tasks.', space_after=12)

# ═══════════════════════════════════════════════════════════════════════════════
# 13. MODEL INTERPRETATION
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('13. Model Interpretation', 1)

doc.add_heading('13.1 Logistic Regression Coefficients', 2)
add_body(doc, 'After fitting, each of the 45 preprocessed features has a coefficient reflecting its association with the log-odds of churn in the linear model. A positive coefficient means the feature is associated with higher predicted churn probability; a negative coefficient with lower. The absolute magnitude reflects the strength of that association.')
add_body(doc, 'Important caveat: These coefficients describe the model\'s linear fit to the training data. They are associations, not causal effects. The coefficient of Contract_Month-to-month does not mean that changing a customer\'s contract would reduce churn probability by a fixed amount.')
add_figure(doc, 'fig13_lr_coefficients.png', 6.0,
           'Figure 13 — Logistic Regression: Top 20 Feature Coefficients. Orange = positive association with churn log-odds; blue = negative association.')

doc.add_heading('13.2 Random Forest Feature Importances', 2)
add_body(doc, 'Random Forest\'s feature_importances_ reports mean Gini impurity reduction per feature across all 200 trees. Since categorical features are one-hot encoded into multiple columns, their importances are summed back to the original feature level for the aggregated view.')
add_figure(doc, 'fig14_rf_feature_importance.png', 6.5,
           'Figure 14 — Random Forest Feature Importances: individual OHE columns (left) and aggregated by original feature (right). tenure, MonthlyCharges, TotalCharges, and Contract are the most important features.')

doc.add_heading('13.3 Gradient Boosting Feature Importances', 2)
add_body(doc, 'Gradient Boosting exposes the same Gini importance mechanism. Its importance rankings broadly agree with the Random Forest rankings, with tenure, MonthlyCharges, and Contract consistently appearing among the top features.')
add_figure(doc, 'fig15_gb_feature_importance.png', 6.5,
           'Figure 15 — Gradient Boosting Feature Importances: individual OHE columns (left) and aggregated by original feature (right).')

doc.add_heading('13.4 Cross-Model Feature Agreement', 2)
cross_data = [
    ('Feature', 'RF', 'GB', 'LR', 'Consistently Important', True),
    ('tenure', 'Top', 'Top', 'Top', 'Yes', False),
    ('MonthlyCharges', 'High', 'High', 'High', 'Yes', False),
    ('TotalCharges', 'High', 'High', 'High', 'Yes (correlated with tenure)', False),
    ('Contract', 'Top', 'Top', 'Top', 'Yes', False),
    ('InternetService', 'High', 'High', 'Medium', 'Yes', False),
    ('OnlineSecurity', 'Medium', 'Medium', 'High', 'Yes', False),
    ('gender', 'Low', 'Low', 'Low', 'No', False),
    ('PhoneService', 'Low', 'Low', 'Low', 'No', False),
]
tbl10 = doc.add_table(rows=len(cross_data), cols=5)
tbl10.style = 'Table Grid'
for i, row in enumerate(tbl10.rows):
    feat, rf, gb, lr, note, is_header = cross_data[i]
    for j, (cell, txt) in enumerate(zip(row.cells, [feat, rf, gb, lr, note])):
        r = cell.paragraphs[0].add_run(txt)
        r.font.size = Pt(9.5); r.font.bold = is_header
        if is_header: set_cell_bg(cell, '1F4E79'); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        elif i % 2 == 0: set_cell_bg(cell, 'F2F5FA')
doc.add_paragraph()
add_body(doc, 'Caveat: Feature importance describes predictive utility in this dataset — it does not establish causal influence on churn. Gini importance can overestimate the importance of correlated features (tenure and TotalCharges, r = 0.83).', space_after=12)

# ═══════════════════════════════════════════════════════════════════════════════
# 14. FINAL MODEL SELECTION
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('14. Final Model Selection', 1)

doc.add_heading('14.1 Selection Criteria', 2)
add_body(doc, 'The primary objective is to identify customers at risk of churning so that targeted retention interventions can be applied. Metrics are prioritised as follows:')
criteria_data = [
    ('Metric', 'Priority', 'Business Rationale', True),
    ('F1-Score', 'Highest', 'Balances Precision and Recall; a model must both catch churners and limit false alarms', False),
    ('Recall (Churn)', 'High', 'Missing a churner (False Negative) is typically the more costly error', False),
    ('ROC-AUC', 'High', 'Threshold-independent ranking; determines effectiveness of risk prioritisation', False),
    ('Precision (Churn)', 'Medium', 'Excessive false alarms waste retention resources', False),
    ('Accuracy', 'Low', 'Misleading on this imbalanced dataset — not used as primary criterion', False),
]
tbl11 = doc.add_table(rows=len(criteria_data), cols=3)
tbl11.style = 'Table Grid'
for i, row in enumerate(tbl11.rows):
    m, p, rat, is_header = criteria_data[i]
    row.cells[0].width = Inches(1.5); row.cells[1].width = Inches(1.0); row.cells[2].width = Inches(4.0)
    for cell, txt in zip(row.cells, [m, p, rat]):
        r = cell.paragraphs[0].add_run(txt)
        r.font.size = Pt(10); r.font.bold = is_header
        if is_header: set_cell_bg(cell, '1F4E79'); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        elif i % 2 == 0: set_cell_bg(cell, 'F2F5FA')
doc.add_paragraph()

doc.add_heading('14.2 Decision: Random Forest Selected', 2)
add_body(doc, 'Random Forest was selected as the final model. It achieves the highest F1-Score (0.6168), the second-highest ROC-AUC (0.8372), and identifies approximately 70% of actual churners (Recall = 0.6989) while maintaining the best Precision among models with competitive Recall (0.5520).')
add_body(doc, 'Logistic Regression achieved a slightly higher ROC-AUC (0.8398) and higher Recall (0.7796) but at the cost of substantially lower Precision (0.5079) — roughly half of all churn predictions are incorrect. Gradient Boosting showed the highest Precision (0.6413) but missed 52% of actual churners (Recall = 0.4758), making it unsuitable as the primary model for retention. Decision Tree was dominated by the other models on all key metrics.')
add_body(doc, 'This selection is based on measured results under baseline hyperparameter configurations. A different business prioritisation (e.g., maximising Recall at all costs) would favour Logistic Regression. The model is not claimed to be universally optimal.', space_after=12)

# ═══════════════════════════════════════════════════════════════════════════════
# 15. FINAL PREDICTION / INFERENCE
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('15. Final Prediction / Inference', 1)
add_body(doc, 'The saved pipeline (models/final_churn_model.joblib) contains the complete fitted Pipeline — ColumnTransformer + RandomForestClassifier. Inference on new customer data requires only loading the file and calling predict() or predict_proba().')
add_body(doc, 'Five synthetic customer records were constructed in Step 9 to demonstrate inference. These records are entirely hypothetical and not from the original dataset.')

pred_data = [
    ('Customer ID', 'Profile', 'Predicted Class', 'Churn Probability', 'Risk Tier', True),
    ('C001', 'Two-year contract, 58m tenure, DSL, security=Yes, bank transfer', 'No Churn', '0.1058', 'Lower', False),
    ('C002', 'Month-to-month, 2m tenure, Fibre optic, security=No, e-check',    'Churn',    '0.8853', 'Higher', False),
    ('C003', 'One-year contract, 24m tenure, DSL, security=Yes, mailed check',  'No Churn', '0.1095', 'Lower', False),
    ('C004', 'Month-to-month, 6m tenure, Fibre optic, security=No, e-check',    'Churn',    '0.9389', 'Higher', False),
    ('C005', 'Two-year contract, 65m tenure, no internet, credit card auto',     'No Churn', '0.0140', 'Lower', False),
]
tbl12 = doc.add_table(rows=len(pred_data), cols=5)
tbl12.style = 'Table Grid'
for i, row in enumerate(tbl12.rows):
    cid, prof, pred, prob, tier, is_header = pred_data[i]
    for j, (cell, txt) in enumerate(zip(row.cells, [cid, prof, pred, prob, tier])):
        r = cell.paragraphs[0].add_run(txt)
        r.font.size = Pt(9.5); r.font.bold = is_header
        if is_header: set_cell_bg(cell, '1F4E79'); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        elif not is_header and pred == 'Churn': set_cell_bg(cell, 'FDECEA')
        elif not is_header: set_cell_bg(cell, 'E8F5E9')
doc.add_paragraph()
add_body(doc, 'Risk tiers (illustrative only — not validated business thresholds): <0.30 = Lower; 0.30–0.60 = Intermediate; >0.60 = Higher. The default classification threshold is 0.50.')
add_body(doc, 'These probabilities are model outputs based on patterns learned from historical training data. They are not guarantees that a customer will or will not churn, and they should not be interpreted as causal statements.', space_after=12)

# ═══════════════════════════════════════════════════════════════════════════════
# 16. LIMITATIONS
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
doc.add_heading('16. Limitations', 1)
for lim in [
    'Single dataset, single time period. The model was trained on one historical snapshot of a single provider\'s customer base. Performance on data from a different provider, geography, or time period is not guaranteed.',
    'No hyperparameter optimisation. All four models use baseline configurations. Systematic cross-validated tuning (e.g., GridSearchCV) has not been applied.',
    'Class imbalance not fully resolved. The 73.6/26.4 ratio is partially addressed through class_weight parameters; SMOTE oversampling and threshold calibration were not implemented.',
    'No temporal validation. The model has not been validated on a future time window (out-of-time testing).',
    'Limited feature set. The model uses only the 19 features in the dataset. Customer service interaction history, lifetime value, or competitor pricing data may add predictive value.',
    'Predictions are not causal. A high predicted churn probability means statistical similarity to past churners — it does not mean any feature caused the customer to churn.',
    'Not production-ready. There is no serving infrastructure, API, model monitoring, drift detection, or retraining pipeline.',
    'Gini importance limitations. Impurity-based importance can overestimate the importance of high-cardinality and correlated features. More robust methods (SHAP values) were not computed.',
    'Default threshold not calibrated. The 0.50 threshold is used throughout. The optimal threshold depends on the relative cost of False Positives and False Negatives, which requires business input.',
]:
    bullet(doc, lim)
doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════════════════════
# 17. FUTURE SCOPE
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('17. Future Scope', 1)
add_body(doc, 'The following improvements are proposed. None have been implemented in the current project.')
for scope in [
    'Hyperparameter optimisation using GridSearchCV or RandomizedSearchCV with stratified k-fold cross-validation on the training set.',
    'Threshold calibration — select an operating threshold based on the business cost ratio of False Negatives to False Positives.',
    'SMOTE oversampling applied within a cross-validation loop to address class imbalance more directly.',
    'Additional model families — compare against XGBoost, LightGBM, or CatBoost.',
    'SHAP values for per-prediction local explanations, enabling transparent risk-score communication to business stakeholders.',
    'Out-of-time validation — hold out a future time period to verify temporal stability of model predictions.',
    'Feature engineering — derive composite features (e.g., charges per tenure month, interaction terms between Contract and InternetService).',
    'Model monitoring pipeline — track prediction score distributions and feature statistics over time to detect data drift.',
    'Deployment — build a web-based inference interface (e.g., using Flask or Streamlit) for real-time churn probability scoring.',
]:
    bullet(doc, scope)
doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════════════════════
# 18. CONCLUSION
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('18. Conclusion', 1)
add_body(doc, 'This project demonstrates a complete, reproducible machine learning workflow for customer churn prediction using the Telco Customer Churn dataset. The project was implemented across nine Jupyter notebooks, progressing from raw data inspection through a systematic quality audit, data cleaning, exploratory data analysis, preprocessing pipeline construction, model training, evaluation, interpretation, final model selection, and inference demonstration.')
add_body(doc, 'The primary data quality issues identified were a TotalCharges column stored as a string due to 11 blank values (resolved by type coercion and zero-imputation for tenure-0 customers) and the customerID column (removed as non-predictive). The cleaned dataset contained 7,021 rows with zero missing values.')
add_body(doc, 'EDA revealed that contract type, customer tenure, internet service type, the presence or absence of add-on services, and payment method are all associated with meaningfully different churn rates in this dataset. All findings were stated as statistical associations without causal claims.')

conc_data = [
    ('Model', 'Accuracy', 'Precision', 'Recall', 'F1 Score', 'ROC-AUC', True),
    ('Logistic Regression', '0.7416', '0.5079', '0.7796', '0.6151', '0.8398', False),
    ('Random Forest ★',     '0.7701', '0.5520', '0.6989', '0.6168', '0.8372', False),
    ('Gradient Boosting',   '0.7907', '0.6413', '0.4758', '0.5463', '0.8333', False),
    ('Decision Tree',       '0.7274', '0.4898', '0.7124', '0.5805', '0.8148', False),
]
tbl13 = doc.add_table(rows=5, cols=6)
tbl13.style = 'Table Grid'
for i, row in enumerate(tbl13.rows):
    m, acc, prec, rec, f1, auc, is_header = conc_data[i]
    for j, (cell, txt) in enumerate(zip(row.cells, [m, acc, prec, rec, f1, auc])):
        r = cell.paragraphs[0].add_run(txt)
        r.font.size = Pt(10); r.font.bold = is_header
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
        if is_header: set_cell_bg(cell, '1F4E79'); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        elif i == 2: set_cell_bg(cell, 'E2EFDA')
doc.add_paragraph()
add_body(doc, 'Random Forest was selected as the final model (★) on the basis of its highest F1-Score (0.6168), competitive ROC-AUC (0.8372), and the most balanced trade-off between Recall (0.6989) and Precision (0.5520). The final pipeline (models/final_churn_model.joblib) can be loaded with a single joblib.load() call and applied directly to new 19-column customer data.')
add_body(doc, 'The results and findings are presented as statistical associations observed in the training data. They should not be interpreted as causal conclusions about customer behaviour. The model is intended as a demonstration of the end-to-end machine learning workflow and is not presented as production-ready.', space_after=12)

# ═══════════════════════════════════════════════════════════════════════════════
# 19. REFERENCES
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_heading('19. References', 1)
refs = [
    'Telco Customer Churn Dataset — IBM Watson Analytics Sample Data. Available at: https://www.kaggle.com/datasets/blastchar/telco-customer-churn',
    'Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825–2830. Documentation: https://scikit-learn.org/stable/',
    'The Pandas Development Team (2023). pandas-dev/pandas: Pandas. Documentation: https://pandas.pydata.org/docs/',
    'Harris, C.R. et al. (2020). Array programming with NumPy. Nature, 585, 357–362. Documentation: https://numpy.org/doc/',
    'Hunter, J.D. (2007). Matplotlib: A 2D Graphics Environment. Computing in Science & Engineering, 9(3), 90–95. Documentation: https://matplotlib.org/stable/',
    'Waskom, M.L. (2021). seaborn: statistical data visualization. Journal of Open Source Software, 6(60), 3021. Documentation: https://seaborn.pydata.org/',
    'Joblib Development Team. joblib: Lightweight pipelining. Documentation: https://joblib.readthedocs.io/',
    'Kluyver, T. et al. (2016). Jupyter Notebooks — a publishing format for reproducible computational workflows. Positioning and Power in Academic Publishing, 87–90. Documentation: https://jupyter-notebook.readthedocs.io/',
    'Rahman, F. (2019). "Telco Customer Churn – Logistic Regression". Kaggle. Reference consulted during project development. Available at: https://www.kaggle.com/code/farazrahman/telco-customer-churn-logisticregression',
]
for i, ref in enumerate(refs, 1):
    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(2)
    para.paragraph_format.space_after  = Pt(5)
    para.paragraph_format.left_indent  = Inches(0.4)
    para.paragraph_format.first_line_indent = Inches(-0.4)
    r = para.add_run(f'[{i}]  {ref}')
    r.font.size = Pt(10)

# ── Page numbers ──────────────────────────────────────────────────────────────
add_page_number(doc)

# ── Save ─────────────────────────────────────────────────────────────────────
doc.save(OUT_PATH)
print(f'Saved: {OUT_PATH}')
