import json
from execution_ai.brokers.broker_utils import load_brokers, save_brokers
from execution_ai.brokers.universal_broker import UniversalBroker

class AutoBrokerHandler:
    def scan_and_select(self):
        brokers = load_brokers()
        for broker in brokers:
            if broker.get("enabled"):
                return {
                    "selected": broker["name"],
                    "instance": UniversalBroker(broker["name"])
                }
        return {"selected": None, "instance": None}

    def register_with_broker(self):
        brokers = load_brokers()
        if not brokers:
            print("No brokers found.")
            return {"api_key": None}
        api_key = brokers[0].get("api_key", "FAKE_AUTO_KEY")
        return {"api_key": api_key}
