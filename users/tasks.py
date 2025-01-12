import os
import uuid
from random import randrange

from django.core.mail import send_mail
from redis import Redis

from config.celery import app
from config.settings import EMAIL_HOST


@app.task
def send_email_code(email):
    code = str(randrange(100000, 999999))
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
    r.set(f"code:{email}", code)
    r.expire(f"code:{email}", 300)
    return code


@app.task
def confirm_email(email):
    url = str(uuid.uuid4())
    host = f"http://localhost:8000/user/confirm_email/{url}/"
    send_mail(
        subject="Emailinigzni Tasdiqlang",
        message=f"Tasdiqlash uchun url:{host}",
        from_email=EMAIL_HOST,
        recipient_list=[email],
    )
    r = Redis(decode_responses=True)
    r.set(url, email)
    r.expire(url, 300)


@app.task
def change_password(email):
    url = str(uuid.uuid4())
    host = f"http://localhost:8000/user/change_password/{url}"
    send_mail(
        subject="Parolni O'zgartish uchun",
        message=f"O'zgartirish uchun url:{host}",
        from_email=EMAIL_HOST,
        recipient_list=[email],
    )
    r = Redis(decode_responses=True)
    r.set(url, email)
    r.expire(url, 300)
