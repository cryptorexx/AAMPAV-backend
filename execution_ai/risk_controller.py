class RiskController:
    def __init__(self, max_trade_risk_percent=1.0, max_daily_loss_percent=5.0, max_position_size=0.1):
        self.max_trade_risk_percent = max_trade_risk_percent  # Max risk per trade (as % of balance)
        self.max_daily_loss_percent = max_daily_loss_percent  # Max loss allowed per day (as % of balance)
        self.max_position_size = max_position_size  # Max portion of balance to use per trade
        self.daily_loss = 0

    def reset_daily_loss(self):
        self.daily_loss = 0

    def check_risk(self, balance, trade_cost, estimated_loss):
        # Check position size constraint
        if trade_cost > balance * self.max_position_size:
            return False, "Trade cost exceeds max position size."

        # Check per-trade risk constraint
        max_risk = balance * self.max_trade_risk_percent / 100
        if estimated_loss > max_risk:
            return False, "Estimated loss exceeds max risk per trade."

        # Check daily loss constraint
        if self.daily_loss + estimated_loss > balance * self.max_daily_loss_percent / 100:
            return False, "Exceeded max daily loss limit."

        return True, "Risk accepted."

    def register_loss(self, loss_amount):
        self.daily_loss += loss_amount
