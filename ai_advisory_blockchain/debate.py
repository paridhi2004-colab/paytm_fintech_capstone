import os
from stock_universe import STOCK_UNIVERSE

MOCK_LLM = int(os.getenv("MOCK_LLM", "1"))

def run_debate(ticker="PAYFIN"):
    data = STOCK_UNIVERSE[ticker]
    beta = data["beta"]
    ret = data["analyst_expected_return"]
    std_dev = data["std_dev"]

    bull_arg = f"With an expected return of {ret:.1%} against a beta of {beta:.2f}, this offers attractive risk-adjusted upside."
    bear_arg = f"The high volatility (standard deviation of {std_dev:.1%}) poses significant downside risk given elevated market sensitivity (beta {beta:.2f})."
    synth_arg = f"While {ticker} exhibits strong return potential ({ret:.1%}), its high beta ({beta:.2f}) and volatility ({std_dev:.1%}) require careful position sizing within moderate/conservative portfolios."

    return {
        "ticker": ticker,
        "bull": bull_arg,
        "bear": bear_arg,
        "synthesizer": synth_arg
    }

if __name__ == "__main__":
    print("=== PART C: MULTI-AGENT DEBATE DEMO ===")
    res = run_debate("PAYFIN")
    print(f"Ticker: {res['ticker']}")
    print(f"Bull: {res['bull']}")
    print(f"Bear: {res['bear']}")
    print(f"Synthesizer: {res['synthesizer']}")
