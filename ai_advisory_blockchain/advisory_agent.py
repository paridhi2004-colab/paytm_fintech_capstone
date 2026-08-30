import os
import math
from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN
from investor_profiles import INVESTOR_PROFILES

MOCK_LLM = int(os.getenv("MOCK_LLM", "1"))

def get_stock_data(ticker):
    """Tool call: simulated local lookup"""
    return STOCK_UNIVERSE.get(ticker)

def run_portfolio_agent(profile):
    inv_id = profile["investor_id"]
    risk = profile["risk_tolerance"]
    
    # 1. THINK Stage: Prescribed Mapping Table
    if risk == "Conservative":
        tickers = ["PAYBOND", "PAYGOLD", "PAYRETAIL"]
    elif risk == "Moderate":
        tickers = ["PAYRETAIL", "PAYINFRA", "PAYGOLD"]
    elif risk == "Aggressive":
        tickers = ["PAYTECH", "PAYFIN", "PAYINFRA"]
    else:
        raise ValueError(f"Unknown risk profile: {risk}")

    # 2. ACT Stage: Tool Call lookup
    stock_data = {t: get_stock_data(t) for t in tickers}

    # 3. OBSERVE Stage: Compute CAPM Expected Return & Portfolio Volatility
    weights = {t: 1.0 / 3.0 for t in tickers}
    
    # CAPM E(R_i) = R_f + Beta * (E(R_m) - R_f)
    capm_returns = {}
    for t in tickers:
        beta = stock_data[t]["beta"]
        capm_returns[t] = RISK_FREE_RATE + beta * (MARKET_RETURN - RISK_FREE_RATE)
        
    portfolio_return = sum(weights[t] * capm_returns[t] for t in tickers)
    
    # Portfolio Variance with pairwise correlation rho = 0.3
    # Var(R_p) = sum(w_i^2 * sigma_i^2) + 2 * sum_{i<j} w_i * w_j * rho * sigma_i * sigma_j
    rho = 0.3
    var_p = sum((weights[t] ** 2) * (stock_data[t]["std_dev"] ** 2) for t in tickers)
    
    # Add cross terms
    var_p += 2 * weights[tickers[0]] * weights[tickers[1]] * rho * stock_data[tickers[0]]["std_dev"] * stock_data[tickers[1]]["std_dev"]
    var_p += 2 * weights[tickers[0]] * weights[tickers[2]] * rho * stock_data[tickers[0]]["std_dev"] * stock_data[tickers[2]]["std_dev"]
    var_p += 2 * weights[tickers[1]] * weights[tickers[2]] * rho * stock_data[tickers[1]]["std_dev"] * stock_data[tickers[2]]["std_dev"]
    
    portfolio_std_dev = math.sqrt(var_p)

    # Human-in-the-loop escalation (> 20.0%)
    escalated = portfolio_std_dev > 0.2000

    # Narrative Generation
    tickers_str = ", ".join(tickers)
    if MOCK_LLM == 1:
        narrative = f"For {risk} investor {inv_id}, we recommend an allocation across {tickers_str} with an expected portfolio return of {portfolio_return:.1%} and volatility of {portfolio_std_dev:.1%}."
    else:
        narrative = f"Custom LLM Narrative: Allocated {inv_id} to {tickers_str} yielding {portfolio_return:.1%} expected return."

    status = "ESCALATED_TO_HUMAN_ADVISOR" if escalated else "AUTO_APPROVED"

    result = {
        "investor_id": inv_id,
        "risk_tolerance": risk,
        "tickers": tickers,
        "portfolio_return": portfolio_return,
        "portfolio_std_dev": portfolio_std_dev,
        "escalated": escalated,
        "status": status,
        "narrative": narrative
    }
    return result

if __name__ == "__main__":
    print("=== PART A: PORTFOLIO ADVISORY AGENT RUN ===")
    for profile in INVESTOR_PROFILES:
        res = run_portfolio_agent(profile)
        print(f"ID: {res['investor_id']} | Risk: {res['risk_tolerance']} | Volatility: {res['portfolio_std_dev']:.2%} | Status: {res['status']}")
        print(f"   Narrative: {res['narrative']}")
