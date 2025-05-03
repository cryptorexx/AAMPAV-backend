class BaseBroker:
    def connect(self):
        raise NotImplementedError

    def place_order(self, symbol, qty, side, type="market", time_in_force="gtc"):
        raise NotImplementedError

    def get_account_info(self):
        raise NotImplementedError
        
from encryption_utils import load_decrypted_credentials

BROKER_CREDENTIALS = load_decrypted_credentials()
