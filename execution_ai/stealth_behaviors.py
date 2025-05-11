import random
import time

# Broker profiles: adjust behavior per broker characteristics
BROKER_PROFILES = {
    "alpaca": {"delay_range": (1.5, 3.5), "quantity_variance": 0.05},
    "binance": {"delay_range": (0.5, 2.0), "quantity_variance": 0.03},
    "default": {"delay_range": (1.0, 2.5), "quantity_variance": 0.02}
}

def apply_stealth(symbol, side, quantity, price, broker_name="default"):
    profile = BROKER_PROFILES.get(broker_name.lower(), BROKER_PROFILES["default"])

    # Fuzz quantity
    fuzz_percent = random.uniform(-profile["quantity_variance"], profile["quantity_variance"])
    adjusted_qty = max(1, round(quantity * (1 + fuzz_percent)))

    # Fuzz price within a tolerable boundary
    price_variation = round(price * random.uniform(-0.002, 0.002), 2)
    adjusted_price = max(0.01, round(price + price_variation, 2))

    # Random delay before placing order
    delay = round(random.uniform(*profile["delay_range"]), 2)

    print(f"[STEALTH] Broker: {broker_name} | Qty: {adjusted_qty} | Price: {adjusted_price} | Delay: {delay}s")

    return {
        "symbol": symbol,
        "side": side,
        "quantity": adjusted_qty,
        "price": adjusted_price,
        "delay": delay
    }
