import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.ensemble import IsolationForest

# 1. Load Data
df_app = pd.read_csv("credit_risk_lending_ml/credit_applicants.csv")

# Engineer thin_file indicator
df_app["is_thin_file"] = df_app["credit_bureau_score"].isna().astype(int)

X = df_app.drop(columns=["applicant_id", "default"])
y = df_app["default"]

# 2. Stratified Split (75/25)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Impute median fit ONLY on train set
train_median_bureau = X_train["credit_bureau_score"].median()
X_train["credit_bureau_score"] = X_train["credit_bureau_score"].fillna(train_median_bureau)
X_test["credit_bureau_score"] = X_test["credit_bureau_score"].fillna(train_median_bureau)

# One-Hot Encoding
X_train = pd.get_dummies(X_train, columns=["employment_type"], drop_first=True)
X_test = pd.get_dummies(X_test, columns=["employment_type"], drop_first=True)
X_train, X_test = X_train.align(X_test, join='left', axis=1, fill_value=0)

# Feature Scaling
scaler = StandardScaler()
num_cols = ["age", "monthly_income_inr", "existing_loans_count", "credit_utilization_ratio", 
            "upi_monthly_inflow_inr", "bounced_payments_count", "credit_bureau_score"]

X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()

X_train_scaled[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test_scaled[num_cols] = scaler.transform(X_test[num_cols])

# 3. Model Training
log_reg = LogisticRegression(random_state=42)
dt_clf = DecisionTreeClassifier(random_state=42)

log_reg.fit(X_train_scaled, y_train)
dt_clf.fit(X_train_scaled, y_train)

y_pred_lr = log_reg.predict(X_test_scaled)
y_prob_lr = log_reg.predict_proba(X_test_scaled)[:, 1]

y_pred_dt = dt_clf.predict(X_test_scaled)
y_prob_dt = dt_clf.predict_proba(X_test_scaled)[:, 1]

def eval_metrics(y_true, y_pred, y_prob):
    return {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall": recall_score(y_true, y_pred, zero_division=0),
        "F1 Score": f1_score(y_true, y_pred, zero_division=0),
        "ROC AUC": roc_auc_score(y_true, y_prob)
    }

print("--- MODEL EVALUATION RESULTS ---")
print("Logistic Regression:", eval_metrics(y_test, y_pred_lr, y_prob_lr))
print("Decision Tree:", eval_metrics(y_test, y_pred_dt, y_prob_dt))

# 4. Anomaly Detection (Isolation Forest)
df_txn = pd.read_csv("credit_risk_lending_ml/txn_behaviour.csv")
features_iso = ["txn_hour", "is_new_device", "txn_amount_inr"]

iso_scaler = StandardScaler()
X_iso_scaled = iso_scaler.fit_transform(df_txn[features_iso])

iso_model = IsolationForest(contamination=15/265, random_state=42)
df_txn["anomaly_score"] = iso_model.fit_predict(X_iso_scaled)

flagged = df_txn[df_txn["anomaly_score"] == -1]
seeded_flagged = flagged[flagged["txn_id"].str.startswith("BTXNA")]

print("\n--- ANOMALY DETECTION RESULTS ---")
print(f"Total Flagged Anomalies: {len(flagged)}")
print(f"Seeded Anomalies Flagged: {len(seeded_flagged)} / 15")
