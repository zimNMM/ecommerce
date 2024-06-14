from django import forms
from .models import Order, Review

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['fullname', 'address']

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(label='Rating', min_value=1, max_value=5)
    comment = forms.CharField(label='Review', widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Review
        fields = ['rating', 'comment']