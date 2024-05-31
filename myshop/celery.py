#myshop/celery.py
import os
from celery import Celery

#Celery 프로그램에 대한 기본 장고 설정 모듈을 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
app = Celery('myshop') # app을 셀러리의 마이샵으로 인스턴스를 생성
app.config_from_object('django.conf:settings', namespace='CELERY')
#config_from_object메서드를 사용해서 프로젝트 설정에서 커스컴 구성을 로드
app.autodiscover_tasks()# 애플리케이션의 비동기 작업을 자동으로 검색하도록 셀러리에 지시
