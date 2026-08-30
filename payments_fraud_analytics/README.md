# Payments & Fraud Analytics Capstone

This repository contains the end-to-end data pipeline, database schema, payment reconciliation module, visual dashboard, and merchant risk analysis.

---

## 1. Project Overview & Execution Steps

### Prerequisites
Install the required dependencies using pip:
```bash
pip install pandas numpy matplotlib seaborn openpyxl sqlite3

1.Installation & Run Steps
 * Generate Datasets:
   Run generate_data.py (configured with seed 42) to reproduce the 547-row ledger, merchants, users, and discrepant gateway export CSV files:
   python generate_data.py

 * Execute Reconciliation:
   Run reconcile.py to process the 4 discrepancy categories (missing rows, amount mismatches, status mismatches):
   python reconcile.py

 * Generate Dashboard Charts:
   Run the dashboard visualization code to generate and save all 4 required chart images:
   * headline_scorecards.png
   * trends_layer.png
   * breakdown_layer.png
   * details_layer.png
2. Design Decisions & Methodology
A. Fee-Tier Assumptions & Classification Rules (merchant_workbook.xlsx)
 * Fee Tiers:
   * Tier 1 (1.2% fee): High Volume / Low Risk merchants meeting volume criteria (\ge 20 txns or \ge ₹10,000 GMV) AND maintaining low risk (\le 1.0\% chargeback ratio).
   * Tier 2 (1.8% fee): Standard operational merchants.
   * Tier 3 (2.5% fee): High Risk merchants with elevated chargebacks (> 1.0\%).
 * Classification Cutoffs: Formulated using nested IF/AND conditions alongside fixed-range VLOOKUP (IFERROR handled) and HLOOKUP lookup tables.
B. Database Schema & Query Design (paytm_payments.db)
 * Relational SQLite schema with declared Primary Keys (transaction_id, merchant_id, user_id) and Foreign Keys.
 * Includes \ge 6 SQL queries with outputs covering JOIN, GROUP BY, and filtering clauses.
 * Burner-Account Query: Surfaces all 15 seeded burner account rows (accounts created within 30 days exhibiting immediate chargebacks).
 * Velocity-Attack Query: Surfaces all 8 seeded velocity attack clusters (\ge 3 rapid transactions in close time proximity).
C. Dashboard & Visual Chart Choices
 * Headline Layer: High-level summary scorecards for macro KPI tracking.
 * Trends Layer: Combined continuous daily GMV line chart and discrete daily chargeback bar chart over the 30-day window.
 * Breakdown Layer: Categorical comparison of total GMV by payment method (UPI, Credit Card, Debit Card, Netbanking) and merchant category.
 * Details Layer: Saved table image ranking the top 10 merchants by transaction count, applying red conditional highlighting for any merchant with chargeback_ratio > 1% (HIGH RISK).
3. Written Interpretations of Dashboard Layers
Layer 1: Headline Scorecards
 * Total Captured GMV: Recorded at ₹2,90,382.00 across captured transactions.
 * Overall Success Rate: Calculated at 85.56% for captured ledger transactions.
 * Reconciliation Match Rate: Evaluated at 90.49% under strict matching logic (identical transaction ID, exact amount, and matching status). Discrepancies represent missing records and status mismatches.
 * Chargeback Ratio: Measured at 5.12% platform-wide using the count-based definition (\text{Chargeback Count} / \text{Total Count}).
Layer 2: Daily Trends Layer
 * Captured daily GMV maintains consistent continuous processing across the 30-day monitoring period.
 * Daily chargeback counts highlight distinct localized spikes corresponding directly to the 8 detected velocity attack clusters.
Layer 3: Breakdown Layer
 * Payment Method: UPI and Credit Cards account for the highest total captured GMV volume.
 * Merchant Category: Retail and E-commerce lead overall GMV settlements compared to Utilities and Services.
Layer 4: Details Layer (Top 10 Merchants & Risk Analysis)
 * While top merchants drive primary transaction volume, chargeback ratios vary per merchant.
 * Merchants exceeding the 1.0% chargeback threshold (using count-based, per-merchant scope) are highlighted and flagged as HIGH RISK to trigger immediate fraud holds.
