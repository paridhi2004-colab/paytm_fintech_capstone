import os
import re
from disclosure_snippets import DISCLOSURE_SNIPPETS

MOCK_LLM = int(os.getenv("MOCK_LLM", "1"))

def extract_signals(snippet: str) -> dict:
    doc_id = snippet.split(":")[0].strip()
    text = snippet.split(":", 1)[1].strip().lower()

    # Risk flags
    risk_flags = []
    if "litigation" in text:
        risk_flags.append("litigation")
    if "regulatory" in text or "regulator" in text or "compliance" in text:
        risk_flags.append("regulatory")
    if "customer" in text or "account for" in text:
        risk_flags.append("customer concentration")

    # Hedging detection
    hedging_keywords = ["assuming", "cautiously", "visibility"]
    hedging_detected = any(kw in text for kw in hedging_keywords)

    # Sentiment classification
    if "confident" in text or "approved" in text:
        sentiment = "confident"
    elif "cautious" in text or "cautiously" in text or "uncertainty" in text or "limited" in text:
        sentiment = "cautious"
    else:
        sentiment = "neutral"

    return {
        "doc_id": doc_id,
        "risk_flags": risk_flags,
        "hedging_detected": hedging_detected,
        "sentiment": sentiment
    }

if __name__ == "__main__":
    print("=== PART B: DISCLOSURE EXTRACTION RUN ===")
    for snip in DISCLOSURE_SNIPPETS:
        res = extract_signals(snip)
        print(f"[{res['doc_id']}] Flags: {res['risk_flags']} | Hedging: {res['hedging_detected']} | Sentiment: {res['sentiment']}")
