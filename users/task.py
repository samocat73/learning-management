from dateutil.relativedelta import relativedelta
from users.models import User
from django.utils import timezone
from celery import shared_task


@shared_task
def checking_last_login_date(*args, **kwargs):
    active_interval = timezone.now() - relativedelta(months=4)
    users = User.objects.filter(
        last_login__lt=active_interval,
        is_active=True,
    )
    for user in users:
        user.is_active = False
        user.save()
