from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is successfully paid.
    """
    order = Order.objects.get(id=order_id)
    #인보이스 이메일 생성
    subject = f'My Shop - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])
    #PDF 생성
    html = render_to_string('orders/order/pdf.html', {'order':order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    #PDF 파일 첨부
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    email.send()