# celery_config.py
from celery import Celery
import os

# Initialize Celery
celery = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL', 'redis://default:JWxPWqicyVxlVEwpHJR927Hck1I4PRl1@redis-12216.c245.us-east-1-3.ec2.redns.redis-cloud.com:12216'))
celery.conf.update(
    result_backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://default:JWxPWqicyVxlVEwpHJR927Hck1I4PRl1@redis-12216.c245.us-east-1-3.ec2.redns.redis-cloud.com:12216')
)