from django import forms
from django.utils.translation import gettext_lazy as _

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1,21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int,
                                      label=_('Quantity'))
    #사용자가 1~20 사이의 수량을 선택. 입력값을 정수로 변환하기위해 coerce=int로 설정한 TypedChoiceField사용한다.
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    #이제품의 카트에 있는 기존 수량을 추가할지 , 덮어 쓸지를 표시할 수 있다. 이 필드는 사용자에게 표시하지 않는다.
