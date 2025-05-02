import random
import time
from datetime import datetime

class StealthBehaviors:
    def __init__(self, config=None):
        self.config = config or {
            "min_delay": 0.5,
            "max_delay": 3,
            "active_hours": (7, 22),
            "simulate_typing": True
        }

    def random_delay(self):
        delay = random.uniform(self.config["min_delay"], self.config["max_delay"])
        print(f"[Stealth] Sleeping for {delay:.2f} seconds to mimic human behavior.")
        time.sleep(delay)

    def is_active_hour(self):
        hour = datetime.now().hour
        return self.config["active_hours"][0] <= hour <= self.config["active_hours"][1]

    def should_skip_trade(self):
        # Add randomness to simulate decision fatigue or uncertainty
        skip_chance = random.random()
        if skip_chance < 0.05:
            print("[Stealth] Skipping trade to mimic hesitation.")
            return True
        return False

    def simulate_typing_delay(self, message="Processing trade..."):
        if self.config.get("simulate_typing"):
            print("[Stealth] Simulating typing:")
            for char in message:
                print(char, end='', flush=True)
                time.sleep(random.uniform(0.05, 0.2))
            print()  # newline
