### python/Django 项目说明

本项目主要是为了深度探索 Django admin 管理后台，同时集成多方面功能。

业务功能为：通过使用 django admin 来达到对于职位工作内容，信息收录的增删查改。

定制具体内容如下：

1. 使用 list_display & exclude 调整职位展示内容
1. 使用 list_filter 增加筛选条件
1. 使用 search_fields 增加查询字段
1. 使用 ordering 对内容默认排序
1. 增加 actions， 可以对选中内容进行 csv 导出
1. 实现导入用 excel 收录职位信息的 django management命令
1. 集成 grappelli 样式管理后台
1. 添加钉钉功能消息通知
1. 集成 sentry，开启 sentry 性能采样
1. 启动本地 Celery 异步任务服务 & Flower 监控服务，使用 Celery，异步发送发送钉钉群消息
1. 自定义中间件，使用 ClassMiddleware 来记录日志，上报异常到 Sentry 和 钉钉
1. Django 中使用缓存, 启用整站缓存
1. 使用 rest framework api 暴露 user / job


### 集成 Sentry
```
安装 sentry-sdk
    $ pip install --upgrade sentry-sdk

在 settings/local.py, settings/production.py 中加上 sentry 的初始化配置

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="http://xxx@recruit.xxxx.com:9000/2",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
```

### 集成 Celery

```
$ brew install redis  # on mac
$ sudo apt-get install redis # on ubuntu/debian

$ pip install -U celery
$ pip install "celery[redis,auth,msgpack]"
$ pip install -U flower

### local.py, production.py 里面添加 Celery 配置

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYD_MAX_TASKS_PER_CHILD = 10
CELERYD_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_work.log")
CELERYBEAT_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_beat.log")

启动本地 Celery 异步任务服务 & Flower 监控服务
$ DJANGO_SETTINGS_MODULE=settings.local celery -A recruitment worker -l info

$ DJANGO_SETTINGS_MODULE=settings.local celery -A recruitment flower
```