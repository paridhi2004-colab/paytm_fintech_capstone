# Paytm FinTech Capstone End-to-End Project

This repository contains the complete three-part Paytm FinTech Capstone project, covering payments fraud analytics, credit risk modeling, AI wealth advisory, and blockchain risk governance.

---

### Key Results Summary
- **Payments Analytics:** Identified 3 peak-hour velocity spikes and a 4.2% reconciliation variance from duplicate log anomalies relative to total settlement volume.
- **Credit Risk ML:** Logistic Regression outperformed Decision Trees with a test ROC-AUC of **0.9168 vs. 0.7226**.
- **DCF & Blockchain:** Constructed a 5-year valuation model in Excel alongside a conceptual smart-contract KYC/AML governance framework.

---

## Repository Structure

payments_fraud_analytics/
├── generate_data.py
├── fraud_analysis.py
├── fraud_analytics.xlsx
├── fraud_dashboard.png
└── README.md

credit_risk_lending_ml/
├── generate_data.py
├── train_and_evaluate.py
├── credit_applicants.csv
├── txn_behaviour.csv
└── README.md

ai_advisory_blockchain/
├── stock_universe.py
├── investor_profiles.py
├── disclosure_snippets.py
├── advisory_agent.py
├── extract_disclosure.py
├── debate.py
├── dcf_calculator.py
├── blockchain_risk_note.md
└── README.md

---

## 1. Environment & Setup Instructions

### Python Version & Dependencies
This project uses standard Python libraries (pandas, numpy, scikit-learn, matplotlib). Dependencies are managed via a single consolidated requirements.txt file at the root level.

To install dependencies:
pip install -r requirements.txt

---

## 2. Execution Instructions (Run End-to-End)

### Part 1: Payments Fraud Analytics
cd payments_fraud_analytics
python generate_data.py
python fraud_analysis.py
cd ..

### Part 2: Credit Risk & Lending ML
cd credit_risk_lending_ml
python generate_data.py
python train_and_evaluate.py
cd ..

### Part 3: AI Advisory & Blockchain Risk
cd ai_advisory_blockchain
python advisory_agent.py
python extract_disclosure.py
python debate.py
python dcf_calculator.py
cd ..

---

## 3. High-Level Design Decisions & Written Interpretations

### Part 1 - Payments & Fraud Analytics
- Threshold Tuning: Fraud rules combine static thresholding with multi-factor risk scoring.
- Rule Monotonicity: Risk categories scale predictably from low-volume transfers to high-frequency spikes.

### Part 2 - Credit Risk & Lending ML
- Model Choice: Logistic Regression was selected over Decision Trees (ROC-AUC 0.9168 vs. 0.7226).
- Fair Lending: Implemented Human-in-the-Loop review for thin-file applicants in high-risk tiers.

### Part 3 - AI-Augmented Advisory & Blockchain Risk
- Execution Mode: Runs completely in deterministic, keyless mock mode (MOCK_LLM=1).
- Agent Governance: Automatic human-adviser escalation triggers when portfolio volatility exceeds 20.00%.
- Crypto Recommendation: Recommends 0.0% allocation to cryptocurrency assets based on CAPM principles.
