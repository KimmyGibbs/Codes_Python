from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_mskim.settings')
app = Celery('test_mskim', include=['app1.tasks'])

default_config = 'test_mskim.conf_celery'

app.config_from_object(default_config)
app.autodiscover_tasks()
