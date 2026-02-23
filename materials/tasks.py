from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from users.models import User


@shared_task
def send_information_about_course(email_list):
    send_mail(
        subject="Курс обновлен.",
        message="Курс, на который вы подписаны обновлен.",
        recipient_list=email_list,
        from_email=settings.EMAIL_HOST_USER,
    )


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
