from django import forms
from .models import Order, Payment

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['fullname', 'address']
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['order', 'method']
        widgets = {
            'card_expiry_date': forms.TextInput(attrs={'placeholder': 'MM/YY'}),
        }