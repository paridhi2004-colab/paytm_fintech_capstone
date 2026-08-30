import os

def calculate_dcf():
    # Inputs for Paytm Wealth Advisory Line
    ebit = 120_000_000 # 120M INR
    tax_rate = 0.25
    dna = 15_000_000
    capex = 20_000_000
    delta_nwc = 5_000_000

    # Base FCFF Formula = EBIT * (1 - Tax) + D&A - CapEx - Delta_NWC
    fcff_base = ebit * (1 - tax_rate) + dna - capex - delta_nwc # 80,000,000 INR

    # WACC Calculation
    cost_of_equity = 0.1225 # via CAPM
    cost_of_debt_after_tax = 0.06
    equity_weight = 0.80
    debt_weight = 0.20
    wacc_base = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt_after_tax) # 11.0%

    terminal_growth_base = 0.04 # 4.0% (satisfies wacc - terminal_growth >= 3%)

    # 5-Year Projection
    growth_rates = [0.12, 0.10, 0.08, 0.06, 0.04]
    projected_fcff = []
    curr = fcff_base
    for g in growth_rates:
        curr = curr * (1 + g)
        projected_fcff.append(curr)

    # Base Case Valuation
    pv_fcff = sum(fcff / ((1 + wacc_base) ** (i + 1)) for i, fcff in enumerate(projected_fcff))
    terminal_value = (projected_fcff[-1] * (1 + terminal_growth_base)) / (wacc_base - terminal_growth_base)
    pv_terminal_value = terminal_value / ((1 + wacc_base) ** 5)
    enterprise_value_dcf = pv_fcff + pv_terminal_value

    # 3x3 Sensitivity Grid
    wacc_variants = [wacc_base - 0.01, wacc_base, wacc_base + 0.01]
    g_variants = [terminal_growth_base - 0.01, terminal_growth_base, terminal_growth_base + 0.01]

    sensitivity_grid = {}
    for w in wacc_variants:
        sensitivity_grid[f"{w:.1%}"] = {}
        for g in g_variants:
            pv_f = sum(fcff / ((1 + w) ** (i + 1)) for i, fcff in enumerate(projected_fcff))
            tv = (projected_fcff[-1] * (1 + g)) / (w - g)
            pv_tv = tv / ((1 + w) ** 5)
            sensitivity_grid[f"{w:.1%}"][f"{g:.1%}"] = pv_f + pv_tv

    # EV/EBITDA Cross-Check
    ebitda = ebit + dna # 135M INR
    implied_multiple = enterprise_value_dcf / ebitda

    print(f"Base FCFF: INR {fcff_base:,.2f}")
    print(f"Base WACC: {wacc_base:.2%}")
    print(f"Implied DCF Enterprise Value: INR {enterprise_value_dcf:,.2f}")
    print(f"Implied EV/EBITDA Multiple: {implied_multiple:.2f}x")
    print("\n--- 3x3 Sensitivity Table (EV in INR) ---")
    header = "WACC / Growth	" + "	".join([f"g={g:.1%}" for g in g_variants])
    print(header)
    for w_str, g_dict in sensitivity_grid.items():
        row = f"WACC={w_str}	" + "	".join([f"INR {val/1e6:.2f}M" for val in g_dict.values()])
        print(row)

if __name__ == "__main__":
    calculate_dcf()
