#celery 임포트
from .celery import app as celery_app

__all__ = ['celery_app']