# forms.py

from django import forms
from shop.models import Order, Comment


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'quantity', 'product']

    product_id = forms.IntegerField(widget=forms.HiddenInput())


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email'}),
            'body': forms.Textarea(attrs={'placeholder': 'Your comment', 'rows': 5}),
        }

