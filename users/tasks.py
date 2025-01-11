import os
from random import randrange
from django.core.mail import send_mail
from redis import Redis

from config.celery import app


@app.task
def send_email(email):
    code = randrange(100000, 999999)
    try:
        send_mail(
            "Emailingizni Tasdiqlang",
            f"Sizning tasdiqlash kodingiz: {code},amail qilish muddati 5 daqiqa",
            from_email=os.getenv("EMAIL_HOST_USER"),
            recipient_list=[email],
        )
    except Exception as e:
        raise Exception(f"Xatolik Emailga xabar yuborishda")

    r = Redis(decode_responses=True)
    r.set(f'code:{email}', code)
    r.expire(f'code:{email}', 300)
    return code
