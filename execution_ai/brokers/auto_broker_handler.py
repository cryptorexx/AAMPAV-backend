# execution_ai/brokers/auto_broker_handler.py

from execution_ai.brokers.alpaca_broker import AlpacaBroker
from execution_ai.brokers.base_broker import BaseBroker
from execution_ai.brokers.universal_broker import UniversalBroker

class AutoBrokerHandler:
    def __init__(self):
        self.supported = ["alpaca", "binance", "fxcm"]  # Expand this list freely

    def scan_and_select(self):
        for broker in self.supported:
            instance = UniversalBroker(broker)
            if instance.connected:
                return {"selected": broker, "instance": instance}
        return {"selected": None, "instance": None}

    def register_with_broker(self):
        result = self.scan_and_select()
        return {"broker": result["selected"], "api_key": result["instance"].api_key if result["instance"] else None}

class AutoBrokerHandler:
    def __init__(self):
        self.brokers = {
            "alpaca": AlpacaBroker  # Can add more brokers here
        }
        self.failed_brokers = []

    def scan_and_select(self):
        """
        Iterate over available brokers and return the first healthy one.
        """
        for name, broker_class in self.brokers.items():
            if name in self.failed_brokers:
                continue  # Skip failed brokers
            
            try:
                broker = broker_class()
                # Try a dummy request or health check (extend later)
                if hasattr(broker, "ping") and broker.ping():
                    print(f"[BrokerHandler] Using broker: {name}")
                    return {"selected": name, "status": "ok"}
                else:
                    self.failed_brokers.append(name)
            except Exception as e:
                print(f"[BrokerHandler] Broker '{name}' failed: {e}")
                self.failed_brokers.append(name)

        raise Exception("No valid brokers available.")

    def register_with_broker(self):
        """
        Returns credentials or identity used (simulated).
        """
        return {
            "api_key": "AUTO-GENERATED-KEY",
            "user_id": "BOT-AGENT"
        }
