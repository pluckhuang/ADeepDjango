import os
from .base import *

ALLOWED_HOSTS = ["127.0.0.1","*"]

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY','w$46iie+a8-7f(13#i%v@pa@+fbm^t@fofizy1^m69r8(-h16o3s882')

DEBUG = False
INSTALLED_APPS += (
    #'debug_toolbar', # and other apps for local development
)

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYD_MAX_TASKS_PER_CHILD = 10
CELERYD_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_work.log")
CELERYBEAT_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_beat.log")

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

'''
sentry_sdk.init(
    dsn="http://xxx@...:9000/2",
    integrations=[DjangoIntegration()],
    # performance tracing sample rate, 采样率, 生产环境访问量过大时，建议调小（不用每一个URL请求都记录性能）
    traces_sample_rate=1.0, #

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
'''



STATIC_URL = 'host/static/'
#STATIC_URL = '/static/'


# The URL of AliCloud OSS endpoint
# Refer https://www.alibabacloud.com/help/zh/doc-detail/31837.htm for OSS Region & Endpoint
OSS_ENDPOINT = 'oss-cn-beijing.aliyuncs.com'

DINGTALK_WEB_HOOK_TOKEN = os.environ.get('DINGTALK_WEB_HOOK_TOKEN','')
DINGTALK_WEB_HOOK = "https://oapi.dingtalk.com/robot/send?access_token=%s" % DINGTALK_WEB_HOOK_TOKEN

##########################