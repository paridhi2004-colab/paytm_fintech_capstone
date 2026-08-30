import pandas as pd
import numpy as np

def reconcile_payments(ledger_df, gateway_df):
    ledger_ids = set(ledger_df['transaction_id'])
    gateway_ids = set(gateway_df['transaction_id'])

    missing_in_gateway_ids = ledger_ids - gateway_ids
    missing_in_gateway = ledger_df[ledger_df['transaction_id'].isin(missing_in_gateway_ids)].copy()

    missing_in_ledger_ids = gateway_ids - ledger_ids
    missing_in_ledger = gateway_df[gateway_df['transaction_id'].isin(missing_in_ledger_ids)].copy()

    common_ids = ledger_ids.intersection(gateway_ids)
    
    merged = pd.merge(
        ledger_df[ledger_df['transaction_id'].isin(common_ids)][['transaction_id', 'amount_inr', 'status']],
        gateway_df[gateway_df['transaction_id'].isin(common_ids)][['transaction_id', 'amount_inr', 'status']],
        on='transaction_id',
        suffixes=('_ledger', '_gateway')
    )

    amount_mismatches = merged[~np.isclose(merged['amount_inr_ledger'], merged['amount_inr_gateway'])].copy()
    amount_mismatches['amount_diff'] = amount_mismatches['amount_inr_gateway'] - amount_mismatches['amount_inr_ledger']

    status_mismatches = merged[merged['status_ledger'] != merged['status_gateway']].copy()

    return missing_in_gateway, missing_in_ledger, amount_mismatches, status_mismatches
