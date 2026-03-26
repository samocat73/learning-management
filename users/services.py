import stripe
from django.conf import settings

stripe.api_key = settings.API_KEY_STRIPE


def create_stripe_product(name_product):
    """Создает продукт в страйпе."""
    product = stripe.Product.create(name=name_product)
    return product


def create_stripe_price(amount, id_stripe_product):
    """Создает цену в страйпе."""
    price = stripe.Price.create(
        currency="usd", unit_amount=amount * 100, product=id_stripe_product
    )
    return price


def create_stripe_sessions(id_stripe_price):
    """Создает сессию на оплату в страйпе."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": id_stripe_price, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
