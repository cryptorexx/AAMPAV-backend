# payment_processor.py
import paypalrestsdk
import os

paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": os.getenv("PAYPAL_CLIENT_ID"),
    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET")
})

def create_payment(amount, currency="USD"):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "https://your-frontend-domain.com/payment-success",
            "cancel_url": "https://your-frontend-domain.com/payment-cancel"
        },
        "transactions": [{
            "amount": {
                "total": f"{amount:.2f}",
                "currency": currency
            },
            "description": "AAMPAV Service Payment"
        }]
    })
    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return {"status": "created", "url": link.href}
    return {"status": "failed", "error": payment.error}
