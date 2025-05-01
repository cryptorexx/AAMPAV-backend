class PortfolioManager:
    def __init__(self):
        self.holdings = {}

    def update_holdings(self, symbol, side, quantity):
        if symbol not in self.holdings:
            self.holdings[symbol] = 0

        if side == "buy":
            self.holdings[symbol] += quantity
        elif side == "sell":
            self.holdings[symbol] = max(0, self.holdings[symbol] - quantity)

    def get_holdings(self):
        return self.holdings

    def get_exposure(self):
        total = sum(self.holdings.values())
        return {symbol: round((qty / total), 2) if total > 0 else 0 for symbol, qty in self.holdings.items()}
