from datetime import datetime, timedelta

import stripe
from django.conf import settings
from django_celery_beat.models import IntervalSchedule, PeriodicTask

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


def set_schedule(*args, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )
    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name="Blocking inactive users",
        task="users.task.checking_last_login_date",
    )
