from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from decimal import Decimal
import stripe
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION
def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        #Stripe 결제 세션에 주문 품목 추가
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data':{ # 가격관련 정보
                        'unit_amount':int(item.price * Decimal('100')), # 지불할 센트 단위의 금액
                        'currency':'usd', #결제에 사용할 통화 USD 미국달러
                        'product_data':{ #제품 관련 정보
                            'name':item.product.name, # 제품이름
                         },
                },
                'quantity':item.quantity, # 구매수량
            })
            #stripe 쿠폰
            if order.coupon:
                stripe_coupon = stripe.Coupon.create(
                    name = order.coupon.code,
                    percent_off = order.discount,
                    duration = 'once')
                session_data['discounts'] = [{
                    'coupon':stripe_coupon.id
                }]
        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())

def payment_completed(request):
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')
