# portfolio_manager.py

class PortfolioManager:
    def __init__(self, initial_cash=100000):
        self.holdings = {}  # {symbol: quantity}
        self.average_price = {}  # {symbol: avg_price}
        self.cash = initial_cash

    def update_holdings(self, symbol, side, quantity, price):
        if symbol not in self.holdings:
            self.holdings[symbol] = 0
            self.average_price[symbol] = price

        if side == "buy":
            total_cost = self.holdings[symbol] * self.average_price[symbol] + quantity * price
            self.holdings[symbol] += quantity
            self.average_price[symbol] = total_cost / self.holdings[symbol]
            self.cash -= quantity * price
        elif side == "sell":
            self.holdings[symbol] = max(0, self.holdings[symbol] - quantity)
            self.cash += quantity * price

    def get_holdings(self):
        return self.holdings

    def get_cash(self):
        return round(self.cash, 2)

    def get_exposure(self):
        total_qty = sum(self.holdings.values())
        return {symbol: round((qty / total_qty), 2) if total_qty > 0 else 0 for symbol, qty in self.holdings.items()}

    def get_portfolio_value(self, market_prices: dict):
        value = self.cash
        for symbol, qty in self.holdings.items():
            value += qty * market_prices.get(symbol, self.average_price.get(symbol, 0))
        return round(value, 2)

    def get_unrealized_pnl(self, market_prices: dict):
        pnl = {}
        for symbol, qty in self.holdings.items():
            market_price = market_prices.get(symbol, self.average_price[symbol])
            pnl[symbol] = round((market_price - self.average_price[symbol]) * qty, 2)
        return pnl
