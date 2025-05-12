import paypalrestsdk
import logging

class WalletManager:
    def __init__(self):
        self.trading_wallet = 0.0
        self.profit_wallet = 0.0

        # PayPal configuration
        paypalrestsdk.configure({
            "mode": "sandbox",  # Change to "live" in production
            "client_id": 
            os.getenv("PAYPAL_CLIENT_ID"),
            "client_secret": 
            os.getenv("PAYPAL_CLIENT_SECRET")
        })

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

    def create_paypal_payment(self, amount: float, currency: str = "USD") -> dict:
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "https://your-frontend-domain.com/success",
                "cancel_url": "https://your-frontend-domain.com/cancel"
            },
            "transactions": [{
                "amount": {
                    "total": f"{amount:.2f}",
                    "currency": currency
                },
                "description": "Automated AI Trading Bot Payment"
            }]
        })

        if payment.create():
            approval_url = next((link.href for link in payment.links if link.rel == "approval_url"), None)
            return {
                "status": "created",
                "payment_id": payment.id,
                "approval_url": approval_url
            }
        else:
            logging.error(payment.error)
            return {
                "status": "failed",
                "error": payment.error
            }
