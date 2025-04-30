class RiskController:
    def __init__(self, broker):
        self.broker = broker
        self.max_drawdown = 0.1  # 10%
        self.max_exposure = 20000

    def check_risk(self, symbol, action, quantity, price):
        balance = self.broker.get_balance()
        cost = quantity * price

        if action == "buy" and cost > self.max_exposure:
            return False

        projected_drawdown = cost / (balance + cost)
        if projected_drawdown > self.max_drawdown:
            return False

        return True

