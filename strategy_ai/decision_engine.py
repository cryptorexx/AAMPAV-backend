import requests

class DecisionEngine:
    def __init__(self, analysis_url: str):
        self.analysis_url = analysis_url

    def analyze_and_decide(self, symbol: str):
        # Step 1: Get analysis
        try:
            response = requests.post(self.analysis_url, json={"symbol": symbol})
            if response.status_code != 200:
                return {"decision": "hold", "reason": "Failed to analyze symbol"}

            analysis = response.json().get("analysis", {})
            trend = analysis.get("trend")
            confidence = analysis.get("confidence", 0)

            # Step 2: Decision logic
            if trend == "bullish" and confidence >= 0.6:
                return {"decision": "buy", "confidence": confidence}
            elif trend == "bearish" and confidence >= 0.6:
                return {"decision": "sell", "confidence": confidence}
            else:
                return {"decision": "hold", "confidence": confidence}
        except Exception as e:
            return {"decision": "hold", "reason": f"Error during decision-making: {e}"}
