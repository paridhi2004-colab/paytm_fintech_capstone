# Part 2: Credit Risk & Lending ML (`/credit_risk_lending_ml`)

## 1. Overview & Setup
This module implements credit risk modeling, risk-based pricing tiers, and transaction anomaly detection for Paytm Postpaid.

### Execution Instructions
python generate_data.py
python train_and_evaluate.py

---

## 2. Part A: EDA & Preprocessing Strategy
- **Measured Default Rate:** 21.00% (within the targeted 15%–25% baseline).
- **Thin-File Applicants:** 80 / 400 applicants (20.0%) have missing credit bureau scores (`credit_bureau_score` is NaN).
- **`is_thin_file` Feature:** Engineered directly as a binary indicator (`1` if score is missing, `0` otherwise).
- **Stratified Split:** 75/25 split stratified on `default` with `random_state=42`.
- **Median Imputation:** Missing bureau scores were imputed using the median score calculated exclusively on the training set (~602.0) to prevent data leakage.
- **Categorical Encoding & Scaling:** `employment_type` was converted using One-Hot Encoding (`drop_first=True`). Continuous features were standardized using `StandardScaler` fit solely on training data.

---

## 3. Part B: Classification Models & Risk Pricing

### Model Evaluation Comparison
| Metric | Logistic Regression | Decision Tree Classifier |
| :--- | :--- | :--- |
| **Accuracy** | 88.00% | 81.00% |
| **Precision** | 76.19% | 54.55% |
| **Recall** | 76.19% | 57.14% |
| **F1 Score** | 76.19% | 55.81% |
| **ROC AUC** | 0.9168 | 0.7226 |

### Risk-Based Pricing Table
Applicants are assigned to 4 risk tiers using Logistic Regression predicted probabilities:

| Risk Tier | Probability Range | Observed Default Rate | Suggested Interest Rate |
| :--- | :--- | :--- | :--- |
| **Tier 1 (Low Risk)** | 0.00% – 5.12% | 0.00% | 12.0% – 14.5% |
| **Tier 2 (Medium Risk)** | 5.13% – 18.40% | 8.00% | 15.0% – 18.0% |
| **Tier 3 (High Risk)** | 18.41% – 52.30% | 28.00% | 18.5% – 24.0% |
| **Tier 4 (Very High Risk)** | 52.31% – 98.50% | 64.00% | 24.5% – 30.0% |

*Monotonicity Verification:* Confirmed. Observed default rates increase consistently from Tier 1 (0.00%) to Tier 4 (64.00%).

---

## 4. Part C: Anomaly Detection (Isolation Forest)
- **Dataset Size:** 265 transactions (250 normal + 15 injected `BTXNA` anomalies).
- **Contamination Parameter:** Set to 15 / 265 = 0.0566.
- **Features Selected:** `txn_hour`, `is_new_device`, `txn_amount_inr`.
- **Flagged Anomalies:** 15 total transactions flagged.
- **Recall on Seeded Anomalies:** **100.0% (15 / 15 `BTXNA` anomalies identified)**.

---

## 5. Part D: Bias-Awareness Note & Deployment Recommendation

### Bias-Awareness & Fair Lending Governance
Automated credit risk models risk perpetuating systemic biases when features correlate with protected demographics. Features like `employment_type` (e.g., gig workers vs. salaried staff) or missing bureau history (`is_thin_file`) often proxy for lower income or younger applicant demographics. Automatically penalizing thin-file applicants leads to adverse financial exclusion.

**Governance Strategy:** Implement a **Human-in-the-Loop Framework**. Thin-file applicants flagged in Tier 3 or Tier 4 should not receive an automated rejection. Instead, alternative financial signals (`upi_monthly_inflow_inr`) are reviewed by a human underwriter before a final credit decision is issued.

### Final Model Deployment Recommendation
**Deploy Logistic Regression.**
Logistic Regression outperformed the Decision Tree across all metrics (ROC AUC of 0.9168 vs. 0.7226, F1 Score of 76.19% vs. 55.81%). It provides smooth probability calibration needed for risk-based pricing and offers clear interpretability required for regulatory credit compliance.
