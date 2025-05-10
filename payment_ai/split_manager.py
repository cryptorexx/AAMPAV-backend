class WalletManager:
    def __init__(self):
        self.trading_wallet = 0.0
        self.profit_wallet = 0.0

    def split_and_store(self, amount: float) -> dict:
        trading_part = round(amount * 0.5, 2)
        profit_part = round(amount * 0.5, 2)

        self.trading_wallet += trading_part
        self.profit_wallet += profit_part

        return {
            "trading_wallet": self.trading_wallet,
            "profit_wallet": self.profit_wallet,
            "split": {
                "to_trading": trading_part,
                "to_profit": profit_part
            }
        }

    def get_wallets(self) -> dict:
        return {
            "trading_wallet": self.trading_wallet,
            "profit_wallet": self.profit_wallet
        }

    def reset_wallets(self) -> dict:
        self.trading_wallet = 0.0
        self.profit_wallet = 0.0
        return self.get_wallets()
