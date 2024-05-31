from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created(order_id):
    """
    주문이 성공적으로 생성될 때
    이메일 알림을 보내는 작업을 생성
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name}, \n\n You have successfully placed an order. Your order ID is {order.id}'
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent

