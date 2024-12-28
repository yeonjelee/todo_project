from __future__ import absolute_import, unicode_literals

# Celery가 프로젝트와 함께 시작되도록 설정
from .celery import app as celery_app

__all__ = ('celery_app',)
