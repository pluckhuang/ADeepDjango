from celery import shared_task
from .dingtalk import send

@shared_task
def send_dingtalk_message(message):
    send(message)